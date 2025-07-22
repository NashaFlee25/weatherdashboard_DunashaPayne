from typing import Optional, Dict, Any
from ..api.weather_api import WeatherAPI
from ..services.weather_logger import log_weather_data

class WeatherService:
    def __init__(self):
        self.weather_api = WeatherAPI()

    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        weather_data = self.weather_api.get_weather(city)
        if weather_data:
            log_weather_data(
                city=city,
                temp=weather_data['main']['temp'],
                description=weather_data['weather'][0]['description']
            )
        return weather_data
