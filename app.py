import sqlite3
import os
from flask import Flask, render_template, redirect, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "secret_key_just_for_dev_environment"  # für CSRF nötig

# Pfad zur Users DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "users.sqlite")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(DATABASE)
    with app.open_resource("schema.sql", mode="r") as f:
        db.executescript(f.read())
    db.commit()
    db.close()

@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Datenbank initialisiert.")

@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        pw = form.password.data

        db = get_db()
        cursor = db.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('This email is already registered', 'danger')
            return redirect(url_for('register') + "#modal-overlay")

        pw_hash = generate_password_hash(pw)
        db.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, pw_hash)
        )
        db.commit()

        flash('Account created.', 'success')
        return redirect(url_for('login') + "#modal-overlay")

    # Bei GET oder Validierungsfehlern
    return render_template("modal.html", active="register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        pw = form.password.data

        db = get_db()
        cursor = db.execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], pw):
            flash("Ungültige E-Mail oder Passwort", 'danger')
            return redirect(url_for('login') + "#modal-overlay")

        flash("Login successful!", 'success')
        return redirect(url_for('index'))

    return render_template("modal.html", active="login", form=form)

if __name__ == "__main__":
    app.run(debug=True)


