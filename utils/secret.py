import os
from dotenv import load_dotenv
load_dotenv()

url_token=os.getenv("URL_TOKEN")
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")