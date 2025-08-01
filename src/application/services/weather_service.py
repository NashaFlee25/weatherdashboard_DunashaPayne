"""Weather service implementation."""

import logging
from typing import Optional

from src.domain.interfaces import IWeatherService, IWeatherRepository, ISettingsRepository
from src.domain.models import WeatherData, WeatherComparison


class WeatherService(IWeatherService):
    """Weather service implementing business logic."""
    
    def __init__(self, weather_repo: IWeatherRepository, settings_repo: ISettingsRepository):
        self.weather_repo = weather_repo
        self.settings_repo = settings_repo
        self.logger = logging.getLogger(__name__)
    
    async def get_weather_for_city(self, city: str) -> Optional[WeatherData]:
        """Get weather data for a city."""
        if not city or not city.strip():
            self.logger.warning("Empty city name provided")
            return None
        
        city = city.strip().title()
        weather_data = await self.weather_repo.get_current_weather(city)
        
        if weather_data:
            # Save last searched city
            self.settings_repo.save_last_searched_city(city)
            self.logger.info(f"Successfully retrieved weather for {city}")
        else:
            self.logger.warning(f"Could not retrieve weather for {city}")
        
        return weather_data
    
    async def compare_cities_weather(self, city1: str, city2: str) -> Optional[WeatherComparison]:
        """Compare weather between two cities."""
        if not city1 or not city2:
            self.logger.warning("Both cities must be provided for comparison")
            return None
        
        # Get weather data for both cities
        weather1 = await self.weather_repo.get_current_weather(city1.strip().title())
        weather2 = await self.weather_repo.get_current_weather(city2.strip().title())
        
        if not weather1 or not weather2:
            self.logger.warning("Could not retrieve weather data for both cities")
            return None
        
        # Calculate differences
        temp_diff = weather1.condition.temperature - weather2.condition.temperature
        humidity_diff = weather1.condition.humidity - weather2.condition.humidity
        wind_diff = weather1.condition.wind_speed - weather2.condition.wind_speed
        
        return WeatherComparison(
            location1=weather1,
            location2=weather2,
            temperature_diff=temp_diff,
            humidity_diff=humidity_diff,
            wind_speed_diff=wind_diff
        )
