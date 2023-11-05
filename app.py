from flask import Flask, jsonify
import requests
from utils.secret import *

app = Flask(__name__)

#Function to get an access token
def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    

    try:
        response = requests.post(url_token, data=payload, headers=headers)

        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            return None
    except Exception as e:
        print(f"An error occured : {str(e)}")
        return None

#GET an acces token
@app.route('/get_token', methods=['GET'])
def get_token():
    access_token = get_access_token()
    if access_token:
        return jsonify({"access_token": access_token})
    else:
        return jsonify({"error": "Impossible d'obtenir le token d'accès"}), 500

#GET all countries
@app.route('/countries', methods=['GET'])
def get_countries():
    access_token = get_access_token()
    if access_token:
        url = "https://api.lufthansa.com/v1/mds-references/countries"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
       
        if response.status_code == 200:
            data = response.json()
            
            countries = data.get("CountryResource", [])["Countries"]["Country"]
            
            result = []
            for country in countries:
                country_code = country.get("CountryCode")
                names = country.get("Names", {}).get("Name", [])
                
                # Prendre le premier élément de la liste s'il existe
                country_name = names[0].get('$') if isinstance(names, list) and names else names.get('$') if isinstance(names, dict) else None
                
                # Ajouter le résultat au dictionnaire
                if country_code and country_name:
                    country_data = {
                        "country_code": country_code,
                        "names": country_name
                    }
                    result.append(country_data)

            return result
        else:
            return jsonify({"error": f"Error {response.status_code}: {response.text}"}), 500
    else:
        return jsonify({"error": "Access token error"}), 500

#GET All cities
@app.route('/cities', methods=['GET'])
def get_cities():
    access_token = get_access_token()
    if access_token:
        url = "https://api.lufthansa.com/v1/mds-references/cities"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            raw_data = data.get("CityResource", []).get("Cities",[]).get("City",[])
            
            result = []
            
            for item in raw_data:
                city_code = item.get("CityCode")
                country_code = item.get("CountryCode")
                names = item.get("Names", {}).get("Name", [])
                
                if isinstance(names, list):
                    name = names[0].get('$') if names else None
                else:
                    name = names.get('$') if names else None
                
                city_data = {
                    "city_code": city_code,
                    "country_code": country_code,
                    "name": name
                }
                
                result.append(city_data)
            
            return result
        else:
            return jsonify({"error": f"Error {response.status_code}: {response.text}"}), 500

    
    else:
        return jsonify({"error": "Access token error"}), 500

#GET All airports
@app.route('/airports', methods=['GET'])
def get_airports():
    access_token = get_access_token()
    if access_token:
        url = "https://api.lufthansa.com/v1/mds-references/airports"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()

            raw_data = data.get("AirportResource", []).get("Airports",[]).get("Airport",[])
            
            result=[]
            
            for item in raw_data:
                airport_code=item.get("AirportCode")
                airport_name=item.get("Names", {}).get("Name", [])
                position=item.get("Position").get("Coordinate")
                city_code=item.get("CityCode")
                country_code=item.get("CountryCode")
                location_type=item.get("LocationType")
                utc_offset=item.get("UtcOffset")
                time_zone_id=item.get("TimeZoneId")
                
                if isinstance(airport_name, list):
                    name = airport_name[0].get('$') if airport_name else None
                else:
                    name = airport_name.get('$') if airport_name else None
                
                airport_data = {
                    "airport_name": name,
                    "airport_code":airport_code,
                    "position":position,
                    "city_code":city_code,
                    "country_code":country_code,
                    "location_type":location_type,
                    "utc_offset":utc_offset,
                    "time_zone_id":time_zone_id
                    }
                
                result.append(airport_data)
                            
        return result
    else:
        return jsonify({"error": "Access token error"}), 500

#GET All airlines
@app.route('/airlines', methods=['GET'])
def get_airlines():
    access_token = get_access_token()
    if access_token:
        url = "https://api.lufthansa.com/v1/mds-references/airlines"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
       
            raw_data = data.get("AirlineResource", []).get("Airlines",[]).get("Airline",[])
            
            result=[]
            
            for item in raw_data:
                airline_id=item.get("AirlineID")
                airline_id_icao=item.get("AirlineID_ICAO")
                airline_name=item.get("Names", {}).get("Name", [])
                
                if isinstance(airline_name, list):
                    name = airline_name[0].get('$') if airline_name else None
                else:
                    name = airline_name.get('$') if airline_name else None
                
                airline_data = {
                    "airline_name": name,
                    "airline_id":airline_id,
                    "airline_id_icao":airline_id_icao,
                    }
                
                result.append(airline_data)
                            
        return result
    else:
        return jsonify({"error": "Access token error"}), 500


if __name__ == '__main__':
    app.run(debug=True)
