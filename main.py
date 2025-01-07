import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def get_location():
    '''
    Get the user's latitude and longitude based on their IP address.

    Returns:
        dict: The location data in JSON format.
    '''
    try:
        res = requests.get('https://ipinfo.io/')
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching location data: {e}")
        return None

def get_weather(lat: float, lon: float):
    '''
    Get weather data from OpenWeatherMap API based on the user's
    latitude and longitude.

    Args:
        lat (float): The latitude of the user's location.
        lon (float): The longitude of the user's location.

    Returns:
        dict: The weather data in JSON format.
    '''
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": os.getenv("WEATHER_API_KEY")
        }
        res = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


location_data = get_location()
location = [float(coord) for coord in location_data["loc"].split(",")]

weather_data = get_weather(location[0], location[1])

with open("weather.json", "w") as f:
    json.dump(weather_data, f, indent=4)
