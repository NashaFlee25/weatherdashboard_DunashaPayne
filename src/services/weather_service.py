import requests
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from src.config.config import Config


class WeatherService:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        try:
            params = {
                'q': city,
                'appid': self.API_KEY,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
