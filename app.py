from flask import Flask, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, IngredientSearchForm

app = Flask(__name__)

app.secret_key = "secret_key_just_for_dev_environment"  # für CSRF nötig

import db

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        pw = form.password.data

        db_conn = db.get_db()
        cursor = db_conn.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('This email is already registered', 'danger')
            return redirect(url_for('register') + "#modal-overlay")

        pw_hash = generate_password_hash(pw)
        db_conn.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, pw_hash)
        )
        db_conn.commit()

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

        db_conn = db.get_db()
        cursor = db_conn.execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        )
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password_hash"], pw):
            flash("Incorrect E-Mail or Password", 'danger')
            return redirect(url_for('login') + "#modal-overlay")
        
        #User sessions: https://testdriven.io/blog/flask-sessions/
        session['user_id'] = user["id"]
        flash("Login successful!", 'success')
        return redirect(url_for('index'))

    return render_template("index.html", active="login", form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("index"))

@app.route('/cocktails/<cocktail_id_arg>', methods=['GET'])
def get_cocktail(cocktail_id_arg):
    if cocktail_id_arg != "random" and not cocktail_id_arg.isnumeric():
        # https://www.w3schools.com/python/ref_string_isnumeric.asp
        # provided an unexpected value, e.g. "abc"
        pass # TODO an error page
    cocktail_id = cocktail_id_arg
    db_conn = db.get_db()
    if cocktail_id_arg == "random":
        # search a random cocktail
        cursor = db_conn.execute("""select c.id
        from cocktails c
        ORDER BY RANDOM()
        LIMIT 1""")
        # https://stackoverflow.com/questions/8001109/trying-to-get-one-cells-values-with-mysqldb
        cocktail_id = cursor.fetchone()[0]
    cursor = db_conn.execute("""select c_ingr.id_cocktail,
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
where c_ingr.id_cocktail = ?""", (cocktail_id,))
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
    # if data['id_cocktail'] is None:
    #     # if a cocktail after cocktail-id not found, e.g. "1"
    #     pass # TODO an error page
    if request.args.get('json') is not None:
        return data
    #like herz
    is_liked = False
    if 'user_id' in session:
        cursor = db_conn.execute("""
            SELECT 1 FROM cocktail_likes
            WHERE user_id = ? AND cocktail_id = ?
        """, (session['user_id'], cocktail_id))
        is_liked = cursor.fetchone() is not None
    return render_template("cocktail.html", data=data, is_liked=is_liked)


@app.route('/cocktails/search/ingredient', methods=['GET', 'POST'])
def search_ingr():
    form = IngredientSearchForm()
    data = {'item': '', 'cocktails': [], 'search': 'ingredient'}

    if form.validate_on_submit():
        ingr = form.item.data.strip().lower()
        data['item'] = ingr
        ingr = "%" + ingr + "%"
        db_conn = db.get_db()
        cursor = db_conn.execute("""
            SELECT c_ingr.id_cocktail,
                   ingr.name AS ingr_name,
                   c.name AS cocktail_name,
                   im.image_path
              FROM cocktail_ingr AS c_ingr
                   LEFT JOIN cocktails c ON c.id = c_ingr.id_cocktail
                   LEFT JOIN cocktail_images im ON im.id_cocktail = c_ingr.id_cocktail
                   LEFT JOIN ingredients ingr ON ingr.id = c_ingr.id_ingr
             WHERE lower(ingr.name) LIKE ? GROUP BY c_ingr.id_cocktail
        """, (ingr,))
        results = cursor.fetchall()

        for row in results:
            data['cocktails'].append({
                'id_cocktail': row['id_cocktail'],
                'cocktail_name': row['cocktail_name'],
                'image_path': row['image_path']
            })
    return render_template("search.html", form=form, data=data)


@app.route('/cocktails/complexity', methods=['GET'])
def complexity():
    level = request.args.get('level')
    if level not in ['easy', 'medium', 'hard']:
        return render_template("complexity.html")
    data = {'item': '', 'cocktails': [], 'search': 'complexity'}
    db_conn = db.get_db()
    levels = [0, 3, 6, 12]
    lvl = 1
    if level == "easy":
        lvl = 1
    if level == "medium":
        lvl = 2
    if level == "hard":
        lvl = 3
    cursor = db_conn.execute("""
    select c_ingr.id_cocktail,
       count(c_ingr.cocktail_position) level,
       c.name AS cocktail_name,
       im.image_path
from cocktail_ingr as c_ingr
left join cocktails c ON c.id = c_ingr.id_cocktail
         left join cocktail_images im on im.id_cocktail = c_ingr.id_cocktail     
group by c_ingr.id_cocktail
having level > ? and level <= ?;
    """, (levels[lvl-1],levels[lvl],))
    results = cursor.fetchall()
    data['item'] = level
    for row in results:
        data['cocktails'].append({
            'id_cocktail': row['id_cocktail'],
            'cocktail_name': row['cocktail_name'],
            'image_path': row['image_path']
        })
    if request.args.get('json') is not None:
        return data
    return render_template("search.html", data=data)


@app.route('/cocktails/<int:cocktail_id>/like', methods=['POST'])
def like_cocktail(cocktail_id):
    if 'user_id' not in session:
        flash("Log in to like cocktails.", "warning")
        return redirect(url_for("login") + "#modal-overlay")

    db_conn = db.get_db()
    user_id = session['user_id']

    cursor = db_conn.execute("""
        SELECT 1 FROM cocktail_likes WHERE user_id = ? AND cocktail_id = ?
    """, (user_id, cocktail_id))

    if cursor.fetchone():
        # Bereits geliked dann entfernen
        db_conn.execute("""
            DELETE FROM cocktail_likes WHERE user_id = ? AND cocktail_id = ?
        """, (user_id, cocktail_id))
        flash("Like entfernt!", "info")
    else:
        # Noch nicht geliked dann hinzufügen
        db_conn.execute("""
            INSERT INTO cocktail_likes (user_id, cocktail_id) VALUES (?, ?)
        """, (user_id, cocktail_id))
        flash("Cocktail liked!", "success")

    db_conn.commit()
    return redirect(url_for('get_cocktail', cocktail_id_arg=cocktail_id))


@app.route('/my-likes')
def my_likes():
    #herz sollte eigendlich sowieso nur sichbar sein wenn eingeloggt
    if 'user_id' not in session:
        flash("Log in to view likes.", "warning")
        return redirect(url_for('login') + "#modal-overlay")

    user_id = session['user_id']
    db_conn = db.get_db()
    cursor = db_conn.execute("""
        SELECT c.id AS id_cocktail, c.name AS cocktail_name, im.image_path
        FROM cocktail_likes l
        JOIN cocktails c ON l.cocktail_id = c.id
        LEFT JOIN cocktail_images im ON im.id_cocktail = c.id
        WHERE l.user_id = ?
    """, (user_id,))
    liked_cocktails = cursor.fetchall()

    data = {
        'cocktails': [{
            'id_cocktail': row['id_cocktail'],
            'cocktail_name': row['cocktail_name'],
            'image_path': row['image_path']
        } for row in liked_cocktails],
        'search': 'likes'
    }
    return render_template("likes.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
