"""Domain models for weather data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WeatherCondition:
    """Represents current weather conditions."""
    temperature: float
    humidity: float
    wind_speed: float
    description: str
    pressure: Optional[float] = None
    visibility: Optional[float] = None
    feels_like: Optional[float] = None


@dataclass
class Location:
    """Represents a geographical location."""
    city: str
    country: str
    timezone: Optional[str] = None
    coordinates: Optional[tuple[float, float]] = None


@dataclass
class WeatherData:
    """Complete weather data for a location."""
    location: Location
    condition: WeatherCondition
    timestamp: datetime
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None


@dataclass
class WeatherComparison:
    """Comparison between two weather locations."""
    location1: WeatherData
    location2: WeatherData
    temperature_diff: float
    humidity_diff: float
    wind_speed_diff: float
