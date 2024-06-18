import requests
import json
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

MONZO_API_URL = "https://api.monzo.com"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BANK_ACCOUNT_ID = os.getenv("BANK_ACCOUNT_ID")
EMPLOYER_NAME = os.getenv("EMPLOYER_NAME")


def get_accounts():
    url = f"{MONZO_API_URL}/accounts"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))


def get_balance():
    url = f"{MONZO_API_URL}/balance?account_id={BANK_ACCOUNT_ID}?"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    print(json.dumps(response.json(), indent=2))


six_days_ago = datetime.datetime.now() - datetime.timedelta(days=6)
since_date = six_days_ago.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_recent_pay_amount():
    url = (
        f"{MONZO_API_URL}/transactions?account_id={BANK_ACCOUNT_ID}&since={since_date}"
    )
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    formatted_response = response.json()
    for transaction in formatted_response["transactions"]:
        amount = transaction["amount"]
        description = transaction["description"]
        if f"{EMPLOYER_NAME}" in description.lower():
            return amount
