import requests
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

api_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

AGE = 20
WEIGHT = 54
HEIGHT = 168

exercise_text = input("Tell me which exercise you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

params = {
    "query": exercise_text,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}

response = requests.post(url=api_endpoint, headers=headers, json=params)
result = response.json()
#print(result)

sheety_endpoint = os.getenv("SHEETY_ENDPOINT")

TOKEN = os.getenv("TOKEN")

header = {
    "Authorization": f"Bearer {TOKEN}"
}

date_now = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheety_inputs = {
        "workout": {
            "date": date_now,
            "time": time_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheet_response = requests.post(url=sheety_endpoint, json=sheety_inputs, headers=header)

    print(sheet_response.text)