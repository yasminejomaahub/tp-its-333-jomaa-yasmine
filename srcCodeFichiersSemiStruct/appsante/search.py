import json

def search_patient_by_id(patient_id):
    
    fichier_json = 'patients.json'  
    with open(fichier_json, 'r') as f:
        patients = json.load(f)

    for patient in patients:
        if patient['id'] == patient_id:
            return json.dumps(patient, ensure_ascii=False, indent=4)

    return json.dumps({"error": f"Patient avec id {patient_id} non trouvé"}, ensure_ascii=False, indent=4)


id_cherche = 1
fiche_patient = search_patient_by_id(id_cherche)
print(fiche_patient)
