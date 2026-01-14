from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
import jwt
import datetime
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

SECRET_KEY = "jwt_secret_123"
DB_NAME = "users.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Création table utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Création automatique de l'admin (admin / admin123)
    admin = cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin:
        hashed = bcrypt.generate_password_hash("admin123").decode('utf-8')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', hashed))
        print("✅ Admin créé : User='admin' / Password='admin123'")
    
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username et password requis"}), 400

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (data['username'],)).fetchone()
    conn.close()

    # Vérification du mot de passe haché
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        token = jwt.encode({
            'user': user['username'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Identifiants incorrects"}), 401

if __name__ == '__main__':
    init_db()
    app.run(port=5003, debug=True)