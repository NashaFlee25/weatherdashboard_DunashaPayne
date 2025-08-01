"""Configuration settings for the weather application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WeatherConfig:
    """Weather API configuration."""
    api_key: str
    temperature_units: str = "metric"
    request_timeout: int = 10
    max_retries: int = 3


@dataclass
class UIConfig:
    """UI configuration."""
    window_width: int = 1200
    window_height: int = 800
    theme: str = "default"
    font_family: str = "Arial"
    font_size: int = 12


@dataclass
class AppConfig:
    """Application configuration."""
    weather: WeatherConfig
    ui: UIConfig
    debug_mode: bool = False
    log_level: str = "INFO"
