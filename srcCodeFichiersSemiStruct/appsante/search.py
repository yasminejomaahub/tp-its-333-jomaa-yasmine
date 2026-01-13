from flask import Flask, jsonify, request
import json

app = Flask(__name__)

fichier_json = 'patients.json'
with open(fichier_json, 'r') as f:
    patients = json.load(f)

@app.route('/patient', methods=['GET'])
def get_patient():
    patient_id = request.args.get('id', type=int)
    field = request.args.get('field')

    if patient_id is None:
        return jsonify({"error": "Il faut fournir un paramètre id"})

    for patient in patients:
        if patient['id'] == patient_id:
            if field:
                champs = [f.strip() for f in field.split(',')]
                resultat = {}
                for f in champs:
                    if f in patient:
                        resultat[f] = patient[f]
                    else:
                        resultat[f] = None  
                return jsonify(resultat)
            else:
                return jsonify(patient)

    return jsonify({"error": f"Patient avec id {patient_id} non trouvé"})

if __name__ == '__main__':
    app.run(debug=True)
