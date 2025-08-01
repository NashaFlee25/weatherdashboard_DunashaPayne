"""Domain interfaces and contracts."""

from abc import ABC, abstractmethod
from typing import Optional, List
from .models import WeatherData, Location, WeatherComparison


class IWeatherRepository(ABC):
    """Interface for weather data repository."""
    
    @abstractmethod
    async def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """Get current weather for a location."""
        pass
    
    @abstractmethod
    async def get_weather_forecast(self, location: str, days: int = 5) -> List[WeatherData]:
        """Get weather forecast for a location."""
        pass


class IWeatherService(ABC):
    """Interface for weather business logic."""
    
    @abstractmethod
    async def get_weather_for_city(self, city: str) -> Optional[WeatherData]:
        """Get weather data for a city."""
        pass
    
    @abstractmethod
    async def compare_cities_weather(self, city1: str, city2: str) -> Optional[WeatherComparison]:
        """Compare weather between two cities."""
        pass


class ISettingsRepository(ABC):
    """Interface for user settings storage."""
    
    @abstractmethod
    def get_api_key(self) -> Optional[str]:
        """Get API key."""
        pass
    
    @abstractmethod
    def get_default_units(self) -> str:
        """Get default temperature units."""
        pass
    
    @abstractmethod
    def get_last_searched_city(self) -> Optional[str]:
        """Get last searched city."""
        pass
    
    @abstractmethod
    def save_last_searched_city(self, city: str) -> None:
        """Save last searched city."""
        pass
