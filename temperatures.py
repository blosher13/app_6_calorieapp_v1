import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

weather_api_key = os.getenv('API_KEY')

def get_lattitude_longitude(city, country, key):
    geo_url = 'http://api.openweathermap.org/geo/1.0/direct?'
    geo_params = {
        'q': f'{city}, {country}',
        'limit': 1
    }
    headers = {
        "x-api-key": weather_api_key
    }
    try:
        geo_response = requests.get(url=geo_url, params=geo_params, headers=headers)
        geo_response.raise_for_status()
        # print(f"Status Code: {geo_response.status_code}")

        geo_response_json = geo_response.json()[0]
        if not geo_response_json:
            print('No location data found')
            return None
        else:
            lattitude = geo_response_json['lat']
            longitude = geo_response_json['lon']
            return {
                'lattitude': lattitude, 
                'longitude': longitude
                }

    except Exception as e:
        print('An errors occured: ', e)
        return None

def get_temperature(lattitude, longitude, key):
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?'
    weather_params = {
        'lat': lattitude,
        'lon': longitude
    }
    headers = {
        "x-api-key": key
    }
    weather_response = requests.get(url=weather_url, params=weather_params, headers=headers)
    # print(f"Status Code: {weather_response.status_code}")
    weather_data = weather_response.json()

    current_temp_kelvin = float(weather_data['main']['temp'])
    current_temp_celsius = current_temp_kelvin - 273.15
    return round(current_temp_celsius, 2)