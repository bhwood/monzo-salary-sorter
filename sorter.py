from utils import get_recent_pay_amount
from dotenv import load_dotenv
import os

load_dotenv()

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


item_to_pot_env_key = {
    "monies": "PERSONAL_POT_MONIES",
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


def link_totals_to_pots():
    totals = calculate_totals()
    pot_totals = {}
    for item, total in totals.items():
        env_key = item_to_pot_env_key.get(item)
        if env_key:
            pot_id = os.getenv(env_key)
            if pot_id:
                pot_totals[pot_id] = total
            else:
                print(f"No .env entry found for {item}")
        else:
            print(f"No mapping found for {item}")
    return pot_totals
