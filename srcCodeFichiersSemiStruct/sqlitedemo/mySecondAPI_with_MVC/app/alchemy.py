from app import app
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle étudiant
class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    adresse = db.Column(db.String(120), nullable=False)
    pin = db.Column(db.String(20), nullable=False)

# Crée la table si elle n'existe pas
with app.app_context():
    db.create_all()

# Route formulaire + tableau
@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        nom = request.form['n']
        adresse = request.form['add']
        pin = request.form['pin']
        student = Etudiant(nom=nom, adresse=adresse, pin=pin)
        db.session.add(student)
        db.session.commit()
    
    students = Etudiant.query.all()
    return render_template("new.html", etudiants=students)
