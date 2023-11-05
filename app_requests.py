import requests
from utils.secret import *

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
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"An error occured : {str(e)}")
        return None

# Exemple d'utilisation de la fonction pour obtenir un token
if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        print(f"Token d'accès Lufthansa : {access_token}")
