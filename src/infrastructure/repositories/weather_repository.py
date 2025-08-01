"""Weather repository implementation using OpenWeatherMap API."""

import aiohttp
import logging
from datetime import datetime
from typing import Optional, List

from src.domain.interfaces import IWeatherRepository
from src.domain.models import WeatherData, WeatherCondition, Location
from src.infrastructure.config.settings import WeatherConfig


class WeatherRepository(IWeatherRepository):
    """Implementation of weather repository using OpenWeatherMap API."""
    
    def __init__(self, config: WeatherConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    async def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """Get current weather for a location."""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": location,
                "appid": self.config.api_key,
                "units": self.config.temperature_units
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_current_weather(data)
                    else:
                        self.logger.error(f"API error {response.status} for location: {location}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error fetching weather for {location}: {e}")
            return None
    
    async def get_weather_forecast(self, location: str, days: int = 5) -> List[WeatherData]:
        """Get weather forecast for a location."""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": location,
                "appid": self.config.api_key,
                "units": self.config.temperature_units,
                "cnt": days * 8  # 8 forecasts per day (every 3 hours)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_forecast_data(data)
                    else:
                        self.logger.error(f"Forecast API error {response.status} for location: {location}")
                        return []
                        
        except Exception as e:
            self.logger.error(f"Error fetching forecast for {location}: {e}")
            return []
    
    def _parse_current_weather(self, data: dict) -> WeatherData:
        """Parse API response into WeatherData object."""
        location = Location(
            city=data["name"],
            country=data["sys"]["country"],
            coordinates=(data["coord"]["lat"], data["coord"]["lon"])
        )
        
        condition = WeatherCondition(
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            description=data["weather"][0]["description"],
            pressure=data["main"].get("pressure"),
            feels_like=data["main"].get("feels_like")
        )
        
        return WeatherData(
            location=location,
            condition=condition,
            timestamp=datetime.now(),
            sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]) if "sunrise" in data["sys"] else None,
            sunset=datetime.fromtimestamp(data["sys"]["sunset"]) if "sunset" in data["sys"] else None
        )
    
    def _parse_forecast_data(self, data: dict) -> List[WeatherData]:
        """Parse forecast API response into list of WeatherData objects."""
        forecasts = []
        city_info = data["city"]
        
        for item in data["list"]:
            location = Location(
                city=city_info["name"],
                country=city_info["country"],
                coordinates=(city_info["coord"]["lat"], city_info["coord"]["lon"])
            )
            
            condition = WeatherCondition(
                temperature=item["main"]["temp"],
                humidity=item["main"]["humidity"],
                wind_speed=item["wind"]["speed"],
                description=item["weather"][0]["description"],
                pressure=item["main"].get("pressure"),
                feels_like=item["main"].get("feels_like")
            )
            
            forecasts.append(WeatherData(
                location=location,
                condition=condition,
                timestamp=datetime.fromtimestamp(item["dt"])
            ))
        
        return forecasts
