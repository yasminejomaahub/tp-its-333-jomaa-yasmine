from app import app
from flask import render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_bcrypt import Bcrypt
import jwt, datetime
from functools import wraps



# =====================
# CONFIG
# =====================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'jwt_secret_123'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
swagger = Swagger(app)

# =====================
# MODELES
# =====================

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    etudiants = db.relationship('Etudiant', backref='groupe')

class Etudiant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    adresse = db.Column(db.String(120), nullable=False)
    pin = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groupe.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# =====================
# INITIALISATION BDD
# =====================

with app.app_context():
    db.create_all()

    # Crée le groupe ITS2 si inexistant
    its2 = Groupe.query.filter_by(nom="ITS2").first()
    if not its2:
        its2 = Groupe(nom="ITS2")
        db.session.add(its2)

    # Crée un utilisateur admin par défaut
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        pwd = bcrypt.generate_password_hash("admin123").decode('utf-8')
        admin = User(username="admin", password=pwd)
        db.session.add(admin)

    db.session.commit()

# =====================
# DECORATEUR TOKEN
# =====================

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token') or request.form.get('token')
        if not token:
            return jsonify({"message": "Token manquant"}), 401
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

# =====================
# ROUTES
# =====================

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Se connecter (Récupération Token)
    ---
    tags:
      - Authentification
    parameters:
      - name: username
        in: formData
        type: string
        required: true
        description: Nom d'utilisateur (admin)
      - name: password
        in: formData
        type: string
        required: true
        description: Mot de passe (admin123)
    responses:
      200:
        description: Connexion réussie, Token généré
      401:
        description: Identifiants incorrects
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Identifiants incorrects"}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return render_template("new.html", token=token, etudiants=Etudiant.query.all())

    return render_template('login.html')

@app.route('/new', methods=['GET', 'POST'])
@token_required
def new(current_user=None):
    """
    Ajouter un étudiant (Token requis)
    ---
    tags:
      - Etudiants
    parameters:
      - name: x-access-token
        in: header
        type: string
        required: true
        description: Token JWT reçu au login
      - name: n
        in: formData
        type: string
        required: true
        description: Nom de l'étudiant
      - name: add
        in: formData
        type: string
        required: true
        description: Adresse
      - name: pin
        in: formData
        type: string
        required: true
        description: Code PIN
    responses:
      200:
        description: Étudiant créé
      401:
        description: Token manquant ou invalide
    """
    its2 = Groupe.query.filter_by(nom="ITS2").first()

    if request.method == 'POST':
        student = Etudiant(
            nom=request.form['n'],
            adresse=request.form['add'],
            pin=request.form['pin'],
            group_id=its2.id
        )
        db.session.add(student)
        db.session.commit()

    students = Etudiant.query.all()
    return render_template("new.html", etudiants=students, token=request.form.get('token'))
