from datetime import datetime ,timezone
from utils.secret import *
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
    time = datetime.now(timezone.utc)
    for ele in data:
        ele['insert_at'] = time.strftime('%Y-%m-%d %H:%M')

    collection = db_mongo[collection_name]
    #result = collection.delete_many({})
    result = collection.insert_many(data)
    
    print(f"Inserted IDs: {result.inserted_ids}")



def create_item_one(element, collection):
    #collection = db_mongo[collection_name]

    # Convertir les données en format compatible avec MongoDB
    time = datetime.now(timezone.utc)
    element = convert_to_mongo_compatible(element)
    element ['insert_at'] = time.strftime('%Y-%m-%d %H:%M')

    
    # Insérer l'élément dans la collection MongoDB
    result = collection.insert_one(element)
    
    # Retourner l'ID inséré en tant que chaîne de caractères
    inserted_id = str(result.inserted_id)
    print(f"Inserted ID: {inserted_id}")
    return inserted_id
    
def create_item_flight(data, collection_name ):
    collection = db_mongo[collection_name]
    #collection.delete_many({})
    for ele in data:
        create_item_one(ele, collection)
