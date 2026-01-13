from app import app
from flask import render_template, request, jsonify

### EXO1 - simple API
#@app.route('/api/salutation', methods=['GET'])
#def salutation():
#    return jsonify({
#        "message": "Hello World"
#    })

### EXO2 - API with simple display
#@app.route('/')
#def index():
#    message = "Hello world"
#    return render_template('index.html', message=message)
    

### EXO3 - API with parameters display 

#@app.route('/')
#def index():
#    user={'name':'john','surname':'doe'}
#    return render_template('index.html',title='MDM',utilisateur=user)

### EXO4 - API with parameters retrieved from URL 
#@app.route('/')
#def index():
#    # récupère les paramètres 'name' et 'surname' depuis l'URL
#    name = request.args.get('name', 'John')      # valeur par défaut 'John'
#    surname = request.args.get('surname', 'Doe') # valeur par défaut 'Doe'
#    user = {'name': name, 'surname': surname}
#
#    return render_template('index.html', title='MDM', utilisateur=user)
