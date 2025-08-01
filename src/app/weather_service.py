"""Weather service implementation."""

import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os


class WeatherService:
    """Service for fetching weather data."""
    
    def __init__(self, config):
        """Initialize the weather service."""
        self.config = config
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def get_current_weather(self, city: str) -> Optional[Dict[str, Any]]:
        """Get current weather for a city."""
        if not self.config.is_api_key_valid():
            return self._get_mock_weather_data(city)
        
        try:
            url = self.config.get_weather_url("weather")
            params = self.config.get_request_params(q=city)
            
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            weather_data = self._parse_weather_data(data)
            
            # Log the weather data
            self._log_weather_data(weather_data)
            
            return weather_data
            
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return self._get_mock_weather_data(city)
        except Exception as e:
            print(f"Error processing weather data: {e}")
            return None
    
    def _parse_weather_data(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse API response into standardized format."""
        try:
            return {
                'city': api_data.get('name', 'Unknown'),
                'country': api_data.get('sys', {}).get('country', 'Unknown'),
                'temperature': round(api_data.get('main', {}).get('temp', 0), 1),
                'feels_like': round(api_data.get('main', {}).get('feels_like', 0), 1),
                'description': api_data.get('weather', [{}])[0].get('description', 'Unknown'),
                'humidity': api_data.get('main', {}).get('humidity', 0),
                'pressure': api_data.get('main', {}).get('pressure', 0),
                'wind_speed': api_data.get('wind', {}).get('speed', 0),
                'wind_direction': api_data.get('wind', {}).get('deg', 0),
                'clouds': api_data.get('clouds', {}).get('all', 0),
                'visibility': api_data.get('visibility', 0) / 1000,  # Convert to km
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return None
    
    def _get_mock_weather_data(self, city: str) -> Dict[str, Any]:
        """Return mock weather data when API is unavailable."""
        return {
            'city': city,
            'country': 'Demo',
            'temperature': 20.0,
            'feels_like': 22.0,
            'description': 'clear sky (demo data)',
            'humidity': 60,
            'pressure': 1013,
            'wind_speed': 3.5,
            'wind_direction': 180,
            'clouds': 20,
            'visibility': 10.0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _log_weather_data(self, weather_data: Dict[str, Any]):
        """Log weather data to history file."""
        try:
            log_file = os.path.join(self.data_dir, 'weather_history_Dunasha.csv')
            
            # Create header if file doesn't exist
            if not os.path.exists(log_file):
                with open(log_file, 'w') as f:
                    f.write('timestamp,city,temperature,description\n')
            
            # Append weather data
            with open(log_file, 'a') as f:
                f.write(f"{weather_data['timestamp']},{weather_data['city']},"
                       f"{weather_data['temperature']},{weather_data['description']}\n")
                
        except Exception as e:
            print(f"Error logging weather data: {e}")
    
    def get_forecast(self, city: str, days: int = 5) -> Optional[Dict[str, Any]]:
        """Get weather forecast for a city."""
        if not self.config.is_api_key_valid():
            return self._get_mock_forecast_data(city, days)
        
        try:
            url = self.config.get_weather_url("forecast")
            params = self.config.get_request_params(q=city)
            
            response = requests.get(url, params=params, timeout=self.config.timeout)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_forecast_data(data)
            
        except requests.RequestException as e:
            print(f"Forecast API request failed: {e}")
            return self._get_mock_forecast_data(city, days)
        except Exception as e:
            print(f"Error processing forecast data: {e}")
            return None
    
    def _parse_forecast_data(self, api_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse forecast API response."""
        try:
            forecast_list = []
            for item in api_data.get('list', [])[:15]:  # 5 days, 3-hour intervals
                forecast_list.append({
                    'datetime': item.get('dt_txt', ''),
                    'temperature': round(item.get('main', {}).get('temp', 0), 1),
                    'description': item.get('weather', [{}])[0].get('description', 'Unknown'),
                    'humidity': item.get('main', {}).get('humidity', 0),
                    'wind_speed': item.get('wind', {}).get('speed', 0)
                })
            
            return {
                'city': api_data.get('city', {}).get('name', 'Unknown'),
                'country': api_data.get('city', {}).get('country', 'Unknown'),
                'forecast': forecast_list
            }
        except Exception as e:
            print(f"Error parsing forecast data: {e}")
            return None
    
    def _get_mock_forecast_data(self, city: str, days: int) -> Dict[str, Any]:
        """Return mock forecast data."""
        forecast_list = []
        base_temp = 20.0
        
        for i in range(days * 3):  # 3 entries per day
            forecast_list.append({
                'datetime': f"2025-07-{9+i//3:02d} {6+(i%3)*8:02d}:00:00",
                'temperature': round(base_temp + (i % 7) - 3, 1),
                'description': ['clear sky', 'few clouds', 'scattered clouds'][i % 3],
                'humidity': 50 + (i % 30),
                'wind_speed': 2.0 + (i % 5)
            })
        
        return {
            'city': city,
            'country': 'Demo',
            'forecast': forecast_list
        }
