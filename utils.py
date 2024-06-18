import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

MONZO_API_URL = "https://api.monzo.com"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_accounts():
    url=f"{MONZO_API_URL}/accounts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))

get_accounts()