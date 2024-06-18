from utils import get_recent_pay_amount
from dotenv import load_dotenv
import os
import requests
import uuid

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BANK_ACCOUNT_ID = os.getenv("BANK_ACCOUNT_ID")
MONZO_API_URL = "https://api.monzo.com"

percentages = {
    "monies": 0.4721,
    "shopping": 0.1713,
    "petrol": 0.0791,
    "haircuts": 0.0198,
    "clothing": 0.0264,
    "car_washing": 0.0132,
    "car_expenses": 0.0132,
    "uniform": 0.0053,
    "vape": 0.0211,
    "gifts": 0.0132,
    "hobbies_and_stuff": 0.0527,
}


def calculate_totals():
    salary = get_recent_pay_amount()
    totals = {}
    for item, percentage in percentages.items():
        total = round(percentage * salary)
        totals[item] = total
    return totals


item_to_personal_pot_env_key = {
    "monies": "PERSONAL_POT_MONIES",
}

item_to_joint_pot_env_key = {
    "shopping": "JOINT_POT_FOOD_SHOPPING",
    "petrol": "JOINT_POT_PETROL",
    "haircuts": "JOINT_POT_HAIR_DRESSING",
    "clothing": "JOINT_POT_CLOTHES_SHOPPING",
    "car_washing": "JOINT_POT_CAR_WASHING",
    "car_expenses": "JOINT_POT_CAR_EXPENSES",
    "uniform": "JOINT_POT_UNIFORM",
    "vape": "JOINT_POT_VAPING",
    "gifts": "JOINT_POT_GIFTS",
    "hobbies_and_stuff": "JOINT_POT_HOBBIES__STUFF",
}


def link_totals_to_personal_pots():
    totals = calculate_totals()
    personal_pot_totals = {}
    for item, total in totals.items():
        env_key = item_to_personal_pot_env_key.get(item)
        if env_key:
            pot_id = os.getenv(env_key)
            if pot_id:
                personal_pot_totals[pot_id] = total
    return personal_pot_totals

def link_totals_to_joint_pots():
    totals = calculate_totals()
    joint_pot_totals = {}
    for item, total in totals.items():
        env_key = item_to_joint_pot_env_key.get(item)
        if env_key:
            pot_id = os.getenv(env_key)
            if pot_id:
                joint_pot_totals[pot_id] = total
    return joint_pot_totals

def sum_personal_values():
    dictionary = link_totals_to_personal_pots()
    value = sum(dictionary.values())/100
    return value

def sum_joint_values():
    dictionary = link_totals_to_joint_pots()
    value = sum(dictionary.values())/100
    return value


def transfer_to_personal_pots():
    pot_totals = link_totals_to_personal_pots()
    for pot_id, amount in pot_totals.items():
        dedupe_id = str(uuid.uuid4())
        url = f"{MONZO_API_URL}/pots/{pot_id}/deposit"
        headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
        data = {
            "source_account_id": {BANK_ACCOUNT_ID},
            "amount": amount,
            "dedupe_id": dedupe_id,
        }
        response = requests.put(url, headers=headers, data=data)
        joint_value_feed_item()
        if response.status_code == 200:
            print(f"Successfully transferred {amount} to pot {pot_id}")
        else:
            print(
                f"Failed to transfer {amount} to pot {pot_id}. Response: {response.text}"
            )

def joint_value_feed_item():
    personal_value = sum_personal_values()
    joint_value = sum_joint_values()
    url = f"{MONZO_API_URL}/feed"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    data = {
        "account_id": {BANK_ACCOUNT_ID},
        "type": "basic",
        "params[title]": "Please Transfer Money to the Joint Account",
        "params[body]": f"Please transfer £{joint_value} to the joint account, £{personal_value} has already been transferred to the correct pot.",
        "params[image_url]": "https://i.ytimg.com/vi/Q5VJePDSXlQ/maxresdefault.jpg",
        "params[background_color]": "#FCF1EE",
        "params[body_color]": "#FCF1EE",
        "params[title_color]": "#333333",
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()