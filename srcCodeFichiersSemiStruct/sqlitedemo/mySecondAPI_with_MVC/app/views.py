from app import app
from flask import render_template, request
import sqlite3
import os
DB = os.path.join(os.path.dirname(__file__), "database.db")

def get_db():
    return sqlite3.connect(DB)

def init_db():
    con = get_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            addr TEXT,
            pin TEXT
        )
    """)
    con.commit()
    con.close()

init_db()

@app.route('/new', methods=['GET', 'POST'])
def new():
    con = get_db()
    cur = con.cursor()

    # Si formulaire POST → ajouter étudiant
    if request.method == 'POST':
        nom = request.form['n']
        addr = request.form['add']
        pin = request.form['pin']

        cur.execute(
            "INSERT INTO etudiants (nom, addr, pin) VALUES (?, ?, ?)",
            (nom, addr, pin)
        )
        con.commit()

    # Récupérer tous les étudiants
    cur.execute("SELECT * FROM etudiants")
    etudiants = cur.fetchall()
    con.close()

    # Afficher la page directement avec tous les étudiants
    return render_template("new.html", etudiants=etudiants)
