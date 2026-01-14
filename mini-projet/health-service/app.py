from flask import Flask, request, jsonify
from functools import wraps
import json
import os
import requests
import jwt

app = Flask(__name__)
DATA_FILE = "data.json"
SECRET_KEY = "jwt_secret_123"

# On pointe vers localhost car on est hors Docker
PERSON_SERVICE_URL = "http://127.0.0.1:5001/persons/"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Token manquant"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route('/health/<int:person_id>', methods=['POST'])
@token_required
def update_health(person_id):
    # 1. On récupère le token reçu pour le passer au service Personne
    token = request.headers.get('x-access-token')
    
    # 2. Appel au service Personne pour vérifier si l'ID existe
    try:
        # On transfère le token dans l'appel
        headers = {'x-access-token': token}
        response = requests.get(f"{PERSON_SERVICE_URL}{person_id}", headers=headers)
        
        if response.status_code == 404:
             return jsonify({"error": "Cette personne n'existe pas (Vérifié via Person-Service)"}), 404
        elif response.status_code != 200:
             return jsonify({"error": "Erreur d'accès au service Personne"}), 403

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Le service Personne est éteint !"}), 503

    # 3. Si tout est OK, on sauvegarde
    health_data = request.get_json()
    all_data = load_data()
    all_data[str(person_id)] = health_data
    save_data(all_data)
    
    return jsonify({"message": "Données santé sauvegardées", "data": health_data}), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)