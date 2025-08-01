"""Weather controller for handling UI interactions."""

import asyncio
import logging
from typing import Optional
from tkinter import messagebox

from src.domain.interfaces import IWeatherService
from src.presentation.views.weather_view import WeatherDisplayView, WeatherSearchView, WeatherComparisonView


class WeatherController:
    """Controller for weather-related UI interactions."""
    
    def __init__(self, weather_service: IWeatherService):
        self.weather_service = weather_service
        self.logger = logging.getLogger(__name__)
        self.display_view: Optional[WeatherDisplayView] = None
        self.search_view: Optional[WeatherSearchView] = None
        self.comparison_view: Optional[WeatherComparisonView] = None
    
    def set_views(self, display_view: WeatherDisplayView, 
                  search_view: WeatherSearchView, 
                  comparison_view: WeatherComparisonView):
        """Set the views this controller manages."""
        self.display_view = display_view
        self.search_view = search_view
        self.comparison_view = comparison_view
    
    def search_weather(self, city: str):
        """Handle weather search request."""
        if not city.strip():
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        # Run async operation in a thread-safe way
        asyncio.create_task(self._async_search_weather(city))
    
    def compare_cities(self, city1: str, city2: str):
        """Handle city comparison request."""
        if not city1.strip() or not city2.strip():
            messagebox.showwarning("Input Error", "Please enter both city names.")
            return
        
        # Run async operation in a thread-safe way
        asyncio.create_task(self._async_compare_cities(city1, city2))
    
    async def _async_search_weather(self, city: str):
        """Async weather search operation."""
        try:
            self.logger.info(f"Searching weather for: {city}")
            weather_data = await self.weather_service.get_weather_for_city(city)
            
            if weather_data and self.display_view:
                self.display_view.display_weather(weather_data)
                self.logger.info(f"Successfully displayed weather for {city}")
            else:
                error_msg = f"Could not retrieve weather data for {city}. Please check the city name and try again."
                if self.display_view:
                    self.display_view.display_error(error_msg)
                messagebox.showerror("Weather Error", error_msg)
                
        except Exception as e:
            error_msg = f"An error occurred while fetching weather data: {str(e)}"
            self.logger.error(error_msg)
            if self.display_view:
                self.display_view.display_error(error_msg)
            messagebox.showerror("Error", error_msg)
    
    async def _async_compare_cities(self, city1: str, city2: str):
        """Async city comparison operation."""
        try:
            self.logger.info(f"Comparing weather between {city1} and {city2}")
            comparison = await self.weather_service.compare_cities_weather(city1, city2)
            
            if comparison and self.display_view:
                self.display_view.display_comparison(comparison)
                self.logger.info(f"Successfully compared {city1} and {city2}")
            else:
                error_msg = f"Could not compare weather between {city1} and {city2}. Please check the city names and try again."
                if self.display_view:
                    self.display_view.display_error(error_msg)
                messagebox.showerror("Comparison Error", error_msg)
                
        except Exception as e:
            error_msg = f"An error occurred while comparing cities: {str(e)}"
            self.logger.error(error_msg)
            if self.display_view:
                self.display_view.display_error(error_msg)
            messagebox.showerror("Error", error_msg)
