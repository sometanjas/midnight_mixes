import sqlite3
#https://docs.python.org/3/library/os.html
import os
#https://flask.palletsprojects.com/en/stable/appcontext/
from flask import g
from app import app

# Pfad zur DB
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "db.sqlite")

def get_db():
    #https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
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

#https://flask.palletsprojects.com/en/stable/cli/
@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Datenbank initialisiert.")