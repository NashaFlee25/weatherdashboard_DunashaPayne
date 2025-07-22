import requests
from typing import Dict, Any, Optional
from ..config.config import API_KEY, BASE_URL

class WeatherAPI:
    def fetch_weather(self, city: str) -> Optional[Dict[str, Any]]:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None
