from utils.secret import *
import pandas as pd

from bson import ObjectId

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

# Fonction pour aplatir les données imbriquées
def flatten_data(data):
    flattened = []
    for item in data:
        flat_item = {}
        for key, value in item.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flat_item[f"{key}_{sub_key}"] = sub_value
            else:
                flat_item[key] = value
        flattened.append(flat_item)
    return flattened

# Récupérez les données de MongoDB
def get_data_from_mongo(collection_name):
    collection = db_mongo[collection_name]
    data = list(collection.find())
    return flatten_data(data)