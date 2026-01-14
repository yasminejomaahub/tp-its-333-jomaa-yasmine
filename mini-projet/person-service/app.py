from flask import Flask, request, jsonify
from functools import wraps
import sqlite3
import jwt

app = Flask(__name__)
SECRET_KEY = "jwt_secret_123"
DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)')
    conn.commit()
    conn.close()

# Décorateur de sécurité
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Token manquant !"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide !"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/persons', methods=['POST'])
@token_required
def create_person():
    data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO persons (name) VALUES (?)', (data['name'],))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": new_id, "name": data['name']}), 201

@app.route('/persons/<int:id>', methods=['GET'])
@token_required
def get_person(id):
    conn = get_db()
    person = conn.execute('SELECT * FROM persons WHERE id = ?', (id,)).fetchone()
    conn.close()
    if person is None:
        return jsonify({"error": "Personne introuvable"}), 404
    return jsonify(dict(person)), 200

if __name__ == '__main__':
    init_db()
    app.run(port=5001, debug=True)