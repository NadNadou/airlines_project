from utils.secret import *
import pandas as pd

def create_item(data, collection_name):
    collection=db_mongo[collection_name]
    result= collection.insert_many(data)
    
    print(f"Inserted IDs: {result.inserted_ids}")
    
    
    