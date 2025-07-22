import requests
from typing import Dict, Any, Optional
from ..config.config import API_KEY

class WeatherAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city: str) -> Optional[Dict[str, Any]]:
        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
