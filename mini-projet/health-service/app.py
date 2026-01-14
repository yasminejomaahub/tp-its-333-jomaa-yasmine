from flask import Flask, request, jsonify
from functools import wraps
import json
import os
import requests
import jwt

app = Flask(__name__)
DATA_FILE = "data.json"
SECRET_KEY = "jwt_secret_123"

# VERSION LOCALE (SANS DOCKER)
# On pointe directement sur le port 5001 de ta machine
PERSON_SERVICE_URL = "http://127.0.0.1:5001/persons/"

def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, 'r') as f:
        try: return json.load(f)
        except: return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f: json.dump(data, f, indent=4)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token: return jsonify({"message": "Token manquant"}), 401
        try: jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except: return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

# Fonction utilitaire pour vérifier si la personne existe (Appel HTTP vers Service Personne)
def check_person_exists(person_id, token):
    headers = {'x-access-token': token}
    try:
        response = requests.get(f"{PERSON_SERVICE_URL}{person_id}", headers=headers)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERREUR: Impossible de contacter le service Personne sur le port 5001")
        return False

# --- ROUTES ---

@app.route('/health/<int:person_id>', methods=['GET'])
@token_required
def get_health(person_id):
    token = request.headers.get('x-access-token')
    # Consigne: Toujours vérifier existence personne
    if not check_person_exists(person_id, token):
        return jsonify({"error": "Personne inexistante ou Service Personne éteint"}), 404

    data = load_data()
    user_data = data.get(str(person_id))
    if not user_data:
        return jsonify({"message": "Pas de données santé pour cet utilisateur"}), 404
    return jsonify(user_data), 200

@app.route('/health/<int:person_id>', methods=['POST', 'PUT'])
@token_required
def update_health(person_id):
    token = request.headers.get('x-access-token')
    if not check_person_exists(person_id, token):
        return jsonify({"error": "Personne inexistante ou Service Personne éteint"}), 404

    health_data = request.get_json()
    all_data = load_data()
    
    # On sauvegarde (écrase ou crée)
    all_data[str(person_id)] = health_data
    save_data(all_data)
    
    return jsonify({"message": "Données sauvegardées", "data": health_data}), 200

@app.route('/health/<int:person_id>', methods=['DELETE'])
@token_required
def delete_health(person_id):
    token = request.headers.get('x-access-token')
    if not check_person_exists(person_id, token):
        return jsonify({"error": "Personne inexistante ou Service Personne éteint"}), 404

    all_data = load_data()
    if str(person_id) in all_data:
        del all_data[str(person_id)]
        save_data(all_data)
        return jsonify({"message": "Données santé supprimées"}), 200
    
    return jsonify({"error": "Rien à supprimer ici"}), 404

if __name__ == '__main__':
    app.run(port=5002, debug=True)