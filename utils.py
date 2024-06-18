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
JOINT_ACCOUNT_ID = os.getenv("JOINT_ACCOUNT_ID")


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


def create_personal_pots_env_files():
    url = f"{MONZO_API_URL}/pots?current_account_id={BANK_ACCOUNT_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    formatted_response = response.json()
    existing_pots = set()
    new_content = ""

    try:
        with open(".env", "r+") as env_file:
            env_content = env_file.read()
            for line in env_content.splitlines():
                if line.startswith("PERSONAL_POT_"):
                    pot_id = line.strip().split("=")[-1].strip("'")
                    existing_pots.add(pot_id)
            for pot in formatted_response["pots"]:
                if not pot["deleted"] and pot["id"] not in existing_pots:
                    sanitised_name = (
                        pot["name"].upper().replace(" ", "_").replace("&", "")
                    )
                    env_line = f"PERSONAL_POT_{sanitised_name}='{pot['id']}'\n"
                    new_content += env_line
            if new_content:
                if not env_content.endswith("\n") and env_content:
                    env_file.write("\n")
                env_file.write(new_content)
    except FileNotFoundError:
        with open(".env", "w") as env_file:
            for pot in formatted_response["pots"]:
                if not pot["deleted"]:
                    sanitised_name = (
                        pot["name"].upper().replace(" ", "_").replace("&", "")
                    )
                    env_line = f"PERSONAL_POT_{sanitised_name}='{pot['id']}'\n"
                    env_file.write(env_line)


def create_joint_pots_env_files():
    url = f"{MONZO_API_URL}/pots?current_account_id={JOINT_ACCOUNT_ID}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)
    formatted_response = response.json()
    existing_pots = set()
    new_content = ""

    try:
        with open(".env", "r+") as env_file:
            env_content = env_file.read()
            for line in env_content.splitlines():
                if line.startswith("JOINT_POT_"):
                    pot_id = line.strip().split("=")[-1].strip("'")
                    existing_pots.add(pot_id)
            for pot in formatted_response["pots"]:
                if not pot["deleted"] and pot["id"] not in existing_pots:
                    sanitised_name = (
                        pot["name"].upper().replace(" ", "_").replace("&", "")
                    )
                    env_line = f"JOINT_POT_{sanitised_name}='{pot['id']}'\n"
                    new_content += env_line
            if new_content:
                if not env_content.endswith("\n") and env_content:
                    env_file.write("\n")
                env_file.write(new_content)
    except FileNotFoundError:
        with open(".env", "w") as env_file:
            for pot in formatted_response["pots"]:
                if not pot["deleted"]:
                    sanitised_name = (
                        pot["name"].upper().replace(" ", "_").replace("&", "")
                    )
                    env_line = f"JOINT_POT_{sanitised_name}='{pot['id']}'\n"
                    env_file.write(env_line)
