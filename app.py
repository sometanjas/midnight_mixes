import sqlite3
import os
from flask import Flask, render_template, redirect, request, url_for, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app = Flask(__name__)
app.secret_key = "secret_key_just_for_dev_environment"  # für CSRF nötig

# Pfad zur DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "db.sqlite")


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
    sql_dir = "sql"
    sql_files = sorted(f for f in os.listdir(sql_dir) if f.endswith('.sql'))
    # loop over sql files and populate database
    for filename in sql_files:
        file_path = os.path.join(sql_dir, filename)
        with app.open_resource(file_path, mode="r") as f:
            db.executescript(f.read())
    db.commit()
    db.close()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Datenbank initialisiert.")


@app.route('/')
def index():
    return render_template("index.html")


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
    return render_template("index.html", active="register", form=form)


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

    return render_template("index.html", active="login", form=form)


@app.route('/cocktails/search/random', methods=['GET'])
def search_cocktail_rand():
    db = get_db()
    # select random cocktail then join related tables and return as a single list
    cursor = db.execute("""select c_ingr.id_cocktail,
       c_ingr.cocktail_position,
       c_ingr.measure,
       ingr.name     ingr_name,
       s.name        snack_name,
       s.content     snack_content,
       s.instruction snack_instruction,
       s.source      snack_source,
       c.name        cocktail_name,
       c.instruction,
       c.category,
       c.glass,
       c.thumb,
       im.image_path
from cocktail_ingr as c_ingr
         left join cocktails c on c.id = c_ingr.id_cocktail
         left join cocktail_images im on im.id_cocktail = c_ingr.id_cocktail
         left join ingredients ingr on ingr.id = c_ingr.id_ingr
         left join snacks s on s.id = ingr.id_snack
where c_ingr.id_cocktail = (select c.id
                            from cocktails c
                                     left join cocktail_images ci on ci.id_cocktail = c.id
                            ORDER BY RANDOM()
                            LIMIT 1);""")
    c = cursor.fetchall()
    data = {'ingrs': [], 'snack': {}}
    # populating the result dataset for the database rows
    for row in c:
        data['id_cocktail'] = row["id_cocktail"]
        data['name'] = row["cocktail_name"]
        data['instruction'] = row["instruction"]
        data['glass'] = row["glass"]
        data['category'] = row["category"]
        data['thumb'] = row["thumb"]
        data['image_path'] = row["image_path"]
        ingr_pos = row["cocktail_position"]
        data['ingrs'].append({
            'cocktail_position': ingr_pos,
            'measure': row["measure"],
            'ingr_name': row["ingr_name"],
        })
        curr_snack_pos = data.get('snack').get('_position')
        snack_name = row["snack_name"]
        # if current row's snack name is none- it means no snack for the ingredient
        if snack_name is None:
            continue
        # curr_snack_pos is None - the initial value. In that case save the snack since there is nothing to compare
        # curr_snack_pos > curr_snack_pos - overwrite snack if its related ingredients' position is less
        if curr_snack_pos is None or curr_snack_pos > curr_snack_pos:
            data['snack'] = {
                'name': snack_name,
                'content': row["snack_content"],
                'instruction': row["snack_instruction"],
                'source': row["snack_source"],
                '_position': ingr_pos,
            }

    if request.args.get('json') is not None:
        return data
    return render_template("cocktail.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
