from app import app
from flask import render_template, request, jsonify

### EXO1 - simple API
#@app.route('/api/salutation', methods=['GET'])
def salutation():
    return jsonify({
        "message": "Hello World"
    })

### EXO2 - API with simple display
@app.route('/route2')
def index2():
    message = "Hello world"
    return render_template('index.html', message=message)
    

### EXO3 - API with parameters display 

@app.route('/route3')
def index3():
    user={'name':'john','surname':'doe'}
    return render_template('index.html',title='MDM',utilisateur=user)

### EXO4 - API with parameters retrieved from URL 
@app.route('/route4')
def index4():
    # récupère les paramètres 'name' et 'surname' depuis l'URL
    name = request.args.get('name', 'John')      
    surname = request.args.get('surname', 'Doe') 
    user = {'name': name, 'surname': surname}
    return render_template('index.html', title='MDM', utilisateur=user)
