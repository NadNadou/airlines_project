
import requests
from mdp import client_id,client_secret
from pprint import pprint
from pymongo import MongoClient
# #-------------------------------PARTIE 1------------------------------------------------
# #---------------------Cretion fonction pour recuperer et traité----------------------------------
# #----------------------------les donées de l'API Lufthnasa-------------------------------------- 

# #------------------Fonction pour recuperer les token------------------------------- 
def get_access_token():
  

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    url_token='https://api.lufthansa.com/v1/oauth/token'
    try:
        response = requests.post(url_token, data=payload, headers=headers)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occured : {str(e)}")
        return None
#----------------------------------------------------------------------------------
    
#------------------Fonction pour recuperer les donées brute ref_data API brute------------------------------- 
#les ref_data dans API Kufthansa sont : countries /cities/airports/airlines/aircrafts
def get_ref_data(ref_data):
    access_token = get_access_token()
    if access_token:
        url = f"https://api.lufthansa.com/v1/mds-references/{ref_data}"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers)
       
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None



# #---------------------------------------------------------------------------------------         

#-----------------------Traitement de données pour chaque ref_data----------------------------                
#-----------cities------------------
def process_city():
    city_data=get_ref_data('cities')['CityResource']['Cities']['City']
    process_data=[]
    for ele in city_data :  
        airport_code=ele['Airports']['AirportCode']
        city_code=ele['CityCode']
        country_code=ele['CountryCode']
        names=ele['Names']['Name'][0]['$'] if isinstance(ele['Names']['Name'],list) else ele['Names']['Name']['$']
        time_zone_id= ele.get('TimeZoneId',None)
        utc_offset=ele['UtcOffset'] 
        process_data.append({'code_aeroport':airport_code,
                             'code_ville':city_code,
                             'code_pays':country_code ,
                             'nom_ville':names,
                             'zone_horaire':time_zone_id,
                             'fuseaux_horaire':utc_offset })
    return process_data    

#-----------------------------------
#-----------countries-----------------
def process_country():
    country_data=get_ref_data('countries')['CountryResource']['Countries']['Country']
    process_data=[] 
    for ele in country_data : 
        country_code=ele['CountryCode']
        names=ele['Names']['Name'][0]['$'] if isinstance(ele['Names']['Name'],list) else ele['Names']['Name']['$']   
        process_data.append({'code_pays_':country_code,
                              'nom_pays':names})
    return process_data
#-----------------------------------
#-----------Airports-----------------
def process_airport():
    airport_data=get_ref_data('airports')['AirportResource']['Airports']['Airport']
    process_data=[]
    for ele in airport_data:
        airport_code=ele['AirportCode']
        city_code=ele['CityCode']
        country_code=ele['CountryCode']
        location_type=ele['LocationType']
        names=ele['Names']['Name'][0]['$'] if isinstance(ele['Names']['Name'],list) else ele['Names']['Name']['$'] 
        position=ele['Position']['Coordinate']
        process_data.append({'code_aeroport':airport_code,
                             'code_ville': city_code,
                             'code_pays':country_code,
                             'location_type':location_type,
                             'nom_aeroport':names,
                             'position_aeroport':position})
    return process_data
#-----------------------------------
#-----------Aircraft-----------------
def process_aircraft():
    aircraft_data=get_ref_data('aircraft')['AircraftResource']['AircraftSummaries']['AircraftSummary']   
    process_data=[]
    for ele in aircraft_data:
        aircraft_code=ele['AircraftCode']
        airline_equipcode=ele['AirlineEquipCode']
        names=ele['Names']['Name']['$'] 
        process_data.append({'code_avion':aircraft_code,
                             'code_equipement':airline_equipcode,
                             'nom_avion':names})
    return process_data
#-----------------------------------
#-----------Airlines-----------------
def process_airlines():
    airlines_data=get_ref_data('airlines')['AirlineResource']['Airlines']['Airline']   
    process_data=[]
    for ele in airlines_data:
        airline_id=ele['AirlineID']
        AirlineID_ICAO=ele.get('AirlineID_ICAO',None)
        names=ele['Names']['Name']['$'] 
        process_data.append({'code_companie':airline_id,
                             'code_ICAO_copmagnie':AirlineID_ICAO,
                             'nom_compagnie':names})
    return process_data
#-----------------------------------

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------




         #-------------------------------PARTIE 2------------------------------------------------
         #--------------------- Inserction de la data traitée----------------------------------
        #-------------------- dans la base de donnée MongoDB -------------------------------------- 

#Après avoir installer l'image de mongodb dans un conteneur docker et lancer le conteneur 

#on va se connecter à la base de donnée mongo et créer une base de donnée
client=MongoClient(host='127.0.0.1',port=27017)
lufthansa_dbc=client['lufthansa_dbc']

#-----------------------Creation de collection et insertion données-------------------------------------------------- 
collection_list=['city', 'country','Airports', 'Aircraft','Airlines']
function_list=[process_city,process_country,process_airport,process_aircraft,process_airlines]
for i in range(len(collection_list)):
    lufthansa_dbc[collection_list[i]].drop()
    collection=lufthansa_dbc.create_collection(collection_list[i])
    collection.insert_many(function_list[i]())
    print('nombre des doc dans ',collection_list[i] ,'est', collection.count_documents({}))

    





