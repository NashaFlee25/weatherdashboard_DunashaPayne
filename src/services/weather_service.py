from typing import Optional, Dict, Any
from ..api.weather_api import WeatherAPI

class WeatherService:
    def __init__(self):
        self.api = WeatherAPI()

    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        data = self.api.fetch_weather(city)
        if data:
            return {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
        return None
