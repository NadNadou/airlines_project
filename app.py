from flask import Flask,jsonify,request
from utils.secret import *
from utils.lufthansa import *
from utils.mongo import *

app = Flask(__name__)


#GET all countries
@app.route('/countries', methods=['GET'])
def get_countries():
    countries = all_countries()
    
    # Vérifier si le résultat est une erreur
    # Si 'countries' est un dictionnaire et contient
    # une clé 'error', retourne une erreur 500
    if isinstance(countries, dict) and "error" in countries:
        # Si c'est une erreur, renvoyer le message d'erreur avec le code 500
        return jsonify(countries), 500
    
    # Si pas d'erreur, renvoyer les données avec le code 200
    return jsonify(countries), 200

@app.route('/cities', methods=['GET'])
def get_cities():
    cities = all_cities()
    
    # Vérifier si le résultat est une erreur
    if isinstance(cities, dict) and "error" in cities:
        # Si c'est une erreur, renvoyer le message d'erreur avec le code 500
        return jsonify(cities), 500
    
    # Si pas d'erreur, renvoyer les données avec le code 200
    return jsonify(cities), 200

@app.route('/airports', methods=['GET'])
def get_airports():
    airports = all_airports()
    
    # Vérifier si le résultat est une erreur
    if isinstance(airports, dict) and "error" in airports:
       return jsonify(airports), 500
    
    # Si pas d'erreur, renvoyer les données avec le code 200
    return jsonify(airports), 200

@app.route('/airlines', methods=['GET'])
def get_airlines():
    airlines = all_airlines()
    
    # Vérifier si le résultat est une erreur
    if isinstance(airlines, dict) and "error" in airlines:
       return jsonify(airlines), 500
    
    # Si pas d'erreur, renvoyer les données avec le code 200
    return jsonify(airlines), 200

@app.route('/schedule', methods=['POST'])
def post_schedule():
    destination = request.args.get('destination')
    origin = request.args.get('origin')
    date = request.args.get('date')
    
    # Format de la requête :
    # localhost:5000/schedule?destination=JFK&origin=FRA&date=2024-05-08
    
    if not all([destination, origin, date]):
        return jsonify({"error": "Missing parameters"}), 400

    schedule = all_schedules(destination=destination, origin=origin, date=date)
    
    
    for item in schedule:
        create_item_one(item, 'flights')

    if isinstance(schedule, dict) and "error" in schedule:
       return jsonify(schedule), 500
    
    return jsonify(schedule), 200

#POST ref data
@app.route('/references', methods=['POST'])
def post_references():
    create_item(all_airports(),'airports')
    create_item(all_cities(),'cities')
    create_item(all_airlines(),'airlines')
    create_item(all_countries(),'countries')

    
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
