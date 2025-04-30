import requests
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

key = os.getenv("WEATHER_KEY")

url = f"https://api.openweathermap.org/data/2.5/weather?lat=44.34&lon=10.99&appid={key}"

b = requests.get(url)

if b.status_code == 200:
    data = b.json()
    print(data["weather"])
else:
    print(f"Error: {b.status_code}, {b.text}")