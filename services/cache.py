"""
Caching service for weather API responses.
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class WeatherCache:
    """
    Simple in-memory cache for weather data.
    Future implementation could use Redis or file-based caching.
    """
    
    def __init__(self, ttl_minutes: int = 10):
        """
        Initialize cache with time-to-live setting.
        
        Args:
            ttl_minutes: Cache time-to-live in minutes
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, city: str) -> Optional[Dict[str, Any]]:
        """
        Get cached weather data for a city.
        
        Args:
            city: City name
            
        Returns:
            Cached weather data or None if not found/expired
        """
        city_key = city.lower().strip()
        
        if city_key not in self._cache:
            return None
        
        cache_entry = self._cache[city_key]
        
        # Check if cache entry is expired
        if datetime.now() - cache_entry['timestamp'] > self._ttl:
            del self._cache[city_key]
            return None
        
        return cache_entry['data']
    
    def set(self, city: str, weather_data: Dict[str, Any]) -> None:
        """
        Cache weather data for a city.
        
        Args:
            city: City name
            weather_data: Weather data to cache
        """
        city_key = city.lower().strip()
        self._cache[city_key] = {
            'data': weather_data,
            'timestamp': datetime.now()
        }
    
    def clear(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
