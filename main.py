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
            "cnt": 4,
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

def is_going_to_rain(id: int):
    '''
    Check if the weather is going to rain based on the weather ID.

    Anything below 700 indicates some form of precipitation (e.g. rain, snow, etc.).

    Args:
        id (int): The weather ID.

    Returns:
        bool: True if it's going to rain, False otherwise.
    '''
    return id < 700


location_data = get_location()

if not location_data:
    # failed to fetch location data...exiting
    exit(1)

location = [float(coord) for coord in location_data["loc"].split(",")]

weather_data = get_weather(location[0], location[1])

if not weather_data:
    # failed to fetch weather data...exiting
    exit(1)

will_rain = False

for forecast in weather_data["list"]:
    for weather in forecast["weather"]:
        id = weather["id"]

        if (is_going_to_rain(id)):
            will_rain = True
            break

if will_rain:
    print("It's going to rain today.")
else:
    print("It's not going to rain today.")
