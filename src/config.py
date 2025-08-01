"""Configuration management for Weather Dashboard."""

import os
from typing import Optional


class WeatherConfig:
    """Configuration manager for the weather dashboard."""
    
    def __init__(self):
        """Initialize configuration."""
        self.api_key = self._load_api_key()
        self.base_url = "http://api.openweathermap.org/data/2.5"
        self.units = "metric"  # metric, imperial, or kelvin
        self.timeout = 10  # API request timeout in seconds
        
    def _load_api_key(self) -> Optional[str]:
        """Load API key from environment or .env file."""
        # Try environment variable first
        api_key = os.getenv('OPENWEATHER_API_KEY')
        
        if not api_key:
            # Try loading from .env file
            env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
            if os.path.exists(env_path):
                try:
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith('OPENWEATHER_API_KEY='):
                                api_key = line.split('=', 1)[1].strip().strip('"\'')
                                break
                except Exception as e:
                    print(f"Error reading .env file: {e}")
        
        if not api_key:
            print("Warning: No API key found. Please set OPENWEATHER_API_KEY environment variable")
            print("or create a .env file with OPENWEATHER_API_KEY=your_key_here")
            # Use demo key for testing (limited functionality)
            api_key = "demo_key"
            
        return api_key
    
    def get_weather_url(self, endpoint: str = "weather") -> str:
        """Get the full API URL for weather requests."""
        return f"{self.base_url}/{endpoint}"
    
    def get_request_params(self, **kwargs) -> dict:
        """Get standard request parameters."""
        params = {
            'appid': self.api_key,
            'units': self.units
        }
        params.update(kwargs)
        return params
    
    def is_api_key_valid(self) -> bool:
        """Check if API key is potentially valid."""
        return self.api_key and self.api_key != "demo_key" and len(self.api_key) > 10
