import requests,json
from utils.secret import *

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



def all_countries():
    access_token = get_access_token()
    if access_token:
        offset=0
        result=[]
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        while True:
            url = f"{baseURL}mds-references/countries?limit={limit_request}&offset={offset}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                countries = data.get("CountryResource", [])["Countries"]["Country"]
                if not countries:  # Sortir de la boucle si aucun pays n'est retourné
                    break
                
                for country in countries:
                    country_code = country.get("CountryCode")
                    names = country.get("Names", {}).get("Name", [])
                    country_name = names[0].get('$') if isinstance(names, list) and names else names.get('$') if isinstance(names, dict) else None
                    
                    if country_code and country_name:
                        country_data = {
                            "country_code": country_code,
                            "names": country_name
                        }
                        result.append(country_data)

                if len(countries) < limit_request:  # Sortir de la boucle si le dernier lot de pays est moins que la limite
                    break
                offset += limit_request
                
                return result
            else:
                return {"error": f"Error {response.status_code}: {response.text}"}
    else:
        return {"error": "Access token error"}
    
    
def all_cities():
    access_token = get_access_token()
    if access_token:
        offset=0
        result=[]
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        while True: 
            url = f"{baseURL}mds-references/cities?limit={limit_request}&offset={offset}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                cities = data.get("CityResource", []).get("Cities",[]).get("City",[])
                
                for item in cities:
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
                    
                if len(cities) < limit_request:  # Sortir de la boucle si le dernier lot de pays est moins que la limite
                    break
                offset += limit_request
                
                return result
            else:
                return {"error": f"Error {response.status_code}: {response.text}"}
    else:
        return {"error": "Access token error"}
       
#GET All airports
def all_airports():
    access_token = get_access_token()
    if access_token:
        offset=0
        result=[]
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        while True : 
            url = f"{baseURL}mds-references/airports?limit={limit_request}&offset={offset}"
            response = requests.get(url, headers=headers)
        
            if response.status_code == 200:
                data = response.json()

                airports = data.get("AirportResource", []).get("Airports",[]).get("Airport",[])

                for item in airports:
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
                    
                if len(airports) < limit_request:  # Sortir de la boucle si le dernier lot de pays est moins que la limite
                    break
                offset += limit_request
                
                return result
            else:
                return {"error": f"Error {response.status_code}: {response.text}"}
    else:
        return {"error": "Access token error"}
       
#GET All airlines
def all_airlines():
    access_token = get_access_token()
    if access_token:
        offset=0
        result=[]
    
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        while True :
            url = f"{baseURL}mds-references/airlines?limit={limit_request}&offset={offset}"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
        
                airlines = data.get("AirlineResource", []).get("Airlines",[]).get("Airline",[])
                
                result=[]
                
                for item in airlines:
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
                if len(airlines) < limit_request:  # Sortir de la boucle si le dernier lot de pays est moins que la limite
                    break
                offset += limit_request
                
                return result
            else:
                return {"error": f"Error {response.status_code}: {response.text}"}
    else:
        return {"error": "Access token error"}
       
#GET All schedules
def all_schedules(origin,destination,date):
    access_token = get_access_token()
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
       
        #Variable settings        
        # origin = 'FRA'
        # destination = 'JFK'
        # date = '2024-03-08'
        
        url = f"{baseURL}operations/schedules/{origin}/{destination}/{date}"         
        print(url)
        print(type(origin))
        
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            flights=data.get('ScheduleResource',[]).get('Schedule',[])

            return flights
        else:
            return {"error": f"Error {response.status_code}: {response.text}"}
    else:
        return {"error": "Access token error"}

      