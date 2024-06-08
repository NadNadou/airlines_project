import os
from dotenv import load_dotenv
load_dotenv()

url_token=os.getenv("URL_TOKEN")
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

baseURL = "https://api.lufthansa.com/v1/"
limit_request = 100

#MongoDB
uri_mongo= os.getenv("URI_MONGO_DB")
client=pymongo.MongoClient(uri_mongo,ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
db_mongo=client[os.getenv("DB_NAME")]


