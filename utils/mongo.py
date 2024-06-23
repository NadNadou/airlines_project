from utils.secret import *
import pandas as pd

from bson import ObjectId
import re

def convert_to_mongo_compatible(data):
    if isinstance(data, list):
        return [convert_to_mongo_compatible(item) for item in data]
    elif isinstance(data, dict):
        return {k: convert_to_mongo_compatible(v) for k, v in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def create_item(data, collection_name):
    collection=db_mongo[collection_name]
    result= collection.insert_many(data)
    
    print(f"Inserted IDs: {result.inserted_ids}")
      
def create_item_one(data, collection_name):
    collection = db_mongo[collection_name]

    # Convertir les données en format compatible avec MongoDB
    data = convert_to_mongo_compatible(data)
    
    # Insérer l'élément dans la collection MongoDB
    result = collection.insert_one(data)
    
    # Retourner l'ID inséré en tant que chaîne de caractères
    inserted_id = str(result.inserted_id)
    print(f"Inserted ID: {inserted_id}")
    return inserted_id

# Fonction pour vérifier si une variable est un dictionnaire
def safe_get(d, key, default=None):
    if isinstance(d, dict):
        return d.get(key, default)
    return default

# Fonction pour convertir une durée de la forme "PT4H40M" en format lisible
def parse_duration(duration):
    pattern = re.compile(r'PT(?:(\d+)H)?(?:(\d+)M)?')
    match = pattern.match(duration)
    if not match:
        return duration  # Retourner la durée d'origine si le format est incorrect

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0

    return f"{hours} h {minutes} min"

def get_from_data():
    collection_flights = db_mongo["flights"]
    data_flights = list(collection_flights.find())
    
    collection_airports = db_mongo["airports"]
    data_airports = pd.DataFrame(list(collection_airports.find()))[['_id','airport_name','airport_code','city_code','country_code','location_type']]
    
    collection_cities = db_mongo["cities"]
    data_cities = pd.DataFrame(list(collection_cities.find()))[['_id','city_code','country_code','name']]
    
    collection_countries = db_mongo["countries"]
    data_countries = pd.DataFrame(list(collection_countries.find()))[['_id','country_code','names']]
    flattened_data = []
    for item in data_flights:
        base = {
            '_id': item.get('_id'),
            'TotalJourney_Duration': safe_get(item.get('TotalJourney'), 'Duration'),
            'insert_at': item.get('insert_at')
        }
        
        # Aplatir chaque vol dans la liste Flight
        for flight in item.get('Flight', []):
            flat_flight = base.copy()
            flat_flight.update({
                'Flight_Departure_AirportCode': safe_get(safe_get(flight, 'Departure'), 'AirportCode'),
                'Flight_Departure_ScheduledTimeLocal_DateTime': safe_get(safe_get(safe_get(flight, 'Departure'), 'ScheduledTimeLocal'), 'DateTime'),
                'Flight_Departure_Terminal_Name': safe_get(safe_get(safe_get(flight, 'Departure'), 'Terminal'), 'Name'),
                'Flight_Arrival_AirportCode': safe_get(safe_get(flight, 'Arrival'), 'AirportCode'),
                'Flight_Arrival_ScheduledTimeLocal_DateTime': safe_get(safe_get(safe_get(flight, 'Arrival'), 'ScheduledTimeLocal'), 'DateTime'),
                'Flight_Arrival_Terminal_Name': safe_get(safe_get(safe_get(flight, 'Arrival'), 'Terminal'), 'Name'),
                'Flight_MarketingCarrier_AirlineID': safe_get(safe_get(flight, 'MarketingCarrier'), 'AirlineID'),
                'Flight_MarketingCarrier_FlightNumber': safe_get(safe_get(flight, 'MarketingCarrier'), 'FlightNumber'),
                'Flight_Equipment_AircraftCode': safe_get(safe_get(flight, 'Equipment'), 'AircraftCode'),
                'Flight_Details_Stops_StopQuantity': safe_get(safe_get(safe_get(flight, 'Details'), 'Stops'), 'StopQuantity'),
                'Flight_Details_DaysOfOperation': safe_get(safe_get(flight, 'Details'), 'DaysOfOperation'),
                'Flight_Details_DatePeriod_Effective': safe_get(safe_get(safe_get(flight, 'Details'), 'DatePeriod'), 'Effective'),
                'Flight_Details_DatePeriod_Expiration': safe_get(safe_get(safe_get(flight, 'Details'), 'DatePeriod'), 'Expiration')
            })
            flattened_data.append(flat_flight)
    df = pd.DataFrame(flattened_data)
    df=df.rename(columns={
        'TotalJourney_Duration':'duration',
        'Flight_Departure_AirportCode':'departure_airportcode',
        'Flight_Departure_ScheduledTimeLocal_DateTime':'departure_scheduled_time',
        'Flight_Departure_Terminal_Name':'departure_terminal_name',
        'Flight_Arrival_AirportCode':'arrival_airportCode',
        'Flight_Arrival_ScheduledTimeLocal_DateTime':'arrival_scheduled_time',
        'Flight_Arrival_Terminal_Name':'arrival_terminal_name',
    })
    
    df_intermediate = df[['_id','duration','insert_at','departure_airportcode','departure_scheduled_time',
                          'departure_terminal_name','arrival_airportCode','arrival_scheduled_time','arrival_terminal_name']].copy()
    
    df_intermediate['duration']=df_intermediate['duration'].apply(parse_duration)
    
    df_ref_data = pd.merge(data_cities[['city_code','country_code','name']],data_countries[['country_code','names']],on="country_code",how='inner')
    df_ref_data = df_ref_data.rename(columns={
        'name':'city_name','names':'country_names'})
    
    df_ref_data = pd.merge(df_ref_data,data_airports[['airport_name','airport_code','city_code','location_type']],on='city_code',how='inner')
    
    # Fusion avec les aéroports pour les informations de départ
    df_intermediate = pd.merge(df_intermediate,df_ref_data,how='inner',left_on='departure_airportcode',right_on='airport_code',suffixes=('','_departure'))
    
    df_intermediate = df_intermediate.rename(columns={
        'airport_name':'departure_airport_name',
        'city_name':'departure_city_name',
        'city_code':'departure_city_code',
        'country_code':'departure_country_code',
        'country_names':'departure_country_names'
    }).drop(columns=['airport_code'])
    
    # Fusion avec les aéroports pour les informations d'arrivée
    df_intermediate = pd.merge(df_intermediate,df_ref_data,how='inner',left_on='arrival_airportCode',right_on='airport_code',suffixes=('','_arrival'))
    df_intermediate = df_intermediate.rename(columns={
        'airport_name':'arrival_airport_name',
        'city_name':'arrival_city_name',
        'city_code':'arrival_city_code',
        'country_code':'arrival_country_code',
        'country_names':'arrival_country_names'
    }).drop(columns=['airport_code'])
    
    unique_departure_cities = df_intermediate['departure_city_name'].unique()
    unique_arrival_cities = df_intermediate['arrival_city_name'].unique()

    combinations_departure_arrival = df_intermediate[["departure_city_name", "arrival_city_name"]].drop_duplicates().to_dict(orient="records")
    
    return unique_departure_cities,unique_arrival_cities,combinations_departure_arrival,df_intermediate