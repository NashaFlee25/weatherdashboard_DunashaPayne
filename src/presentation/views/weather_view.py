"""Weather view components."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from src.domain.models import WeatherData, WeatherComparison


class WeatherDisplayView:
    """View for displaying weather information."""
    
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        """Create display widgets."""
        self.main_frame = ttk.LabelFrame(self.parent, text="Weather Information", padding="15")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.weather_text = tk.Text(
            self.main_frame,
            height=15,
            width=60,
            wrap=tk.WORD,
            font=("Arial", 11),
            state=tk.DISABLED
        )
        
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.weather_text.yview)
        self.weather_text.configure(yscrollcommand=scrollbar.set)
        
        self.weather_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def display_weather(self, weather_data: WeatherData):
        """Display weather data."""
        self.weather_text.config(state=tk.NORMAL)
        self.weather_text.delete(1.0, tk.END)
        
        content = self._format_weather_data(weather_data)
        self.weather_text.insert(1.0, content)
        
        self.weather_text.config(state=tk.DISABLED)
    
    def display_comparison(self, comparison: WeatherComparison):
        """Display weather comparison."""
        self.weather_text.config(state=tk.NORMAL)
        self.weather_text.delete(1.0, tk.END)
        
        content = self._format_comparison_data(comparison)
        self.weather_text.insert(1.0, content)
        
        self.weather_text.config(state=tk.DISABLED)
    
    def display_error(self, message: str):
        """Display error message."""
        self.weather_text.config(state=tk.NORMAL)
        self.weather_text.delete(1.0, tk.END)
        self.weather_text.insert(1.0, f"Error: {message}")
        self.weather_text.config(state=tk.DISABLED)
    
    def clear(self):
        """Clear the display."""
        self.weather_text.config(state=tk.NORMAL)
        self.weather_text.delete(1.0, tk.END)
        self.weather_text.config(state=tk.DISABLED)
    
    def _format_weather_data(self, weather: WeatherData) -> str:
        """Format weather data for display."""
        return f"""🌍 Location: {weather.location.city}, {weather.location.country}
🌡️ Temperature: {weather.condition.temperature}°C
💧 Humidity: {weather.condition.humidity}%
💨 Wind Speed: {weather.condition.wind_speed} m/s
📝 Conditions: {weather.condition.description.title()}
🕐 Updated: {weather.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
{f'🌅 Sunrise: {weather.sunrise.strftime("%H:%M")}' if weather.sunrise else ''}
{f'🌅 Sunset: {weather.sunset.strftime("%H:%M")}' if weather.sunset else ''}
{f'🌡️ Feels Like: {weather.condition.feels_like}°C' if weather.condition.feels_like else ''}
{f'📊 Pressure: {weather.condition.pressure} hPa' if weather.condition.pressure else ''}"""
    
    def _format_comparison_data(self, comparison: WeatherComparison) -> str:
        """Format comparison data for display."""
        return f"""🆚 Weather Comparison

📍 {comparison.location1.location.city}:
   🌡️ Temperature: {comparison.location1.condition.temperature}°C
   💧 Humidity: {comparison.location1.condition.humidity}%
   💨 Wind: {comparison.location1.condition.wind_speed} m/s
   📝 Conditions: {comparison.location1.condition.description.title()}

📍 {comparison.location2.location.city}:
   🌡️ Temperature: {comparison.location2.condition.temperature}°C
   💧 Humidity: {comparison.location2.condition.humidity}%
   💨 Wind: {comparison.location2.condition.wind_speed} m/s
   📝 Conditions: {comparison.location2.condition.description.title()}

📊 Differences:
   🌡️ Temperature: {comparison.temperature_diff:+.1f}°C
   💧 Humidity: {comparison.humidity_diff:+.1f}%
   💨 Wind Speed: {comparison.wind_speed_diff:+.1f} m/s"""


class WeatherSearchView:
    """View for weather search functionality."""
    
    def __init__(self, parent: tk.Widget, on_search: Callable[[str], None]):
        self.parent = parent
        self.on_search = on_search
        self._create_widgets()
    
    def _create_widgets(self):
        """Create search widgets."""
        search_frame = ttk.LabelFrame(self.parent, text="Search Weather", padding="10")
        search_frame.pack(fill="x", padx=10, pady=10)
        
        input_frame = ttk.Frame(search_frame)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="City Name:").pack(side="left", padx=(0, 10))
        
        self.city_entry = ttk.Entry(input_frame, width=25, font=("Arial", 12))
        self.city_entry.pack(side="left", padx=(0, 10))
        self.city_entry.bind("<Return>", self._on_enter_pressed)
        
        self.search_button = ttk.Button(
            input_frame,
            text="Get Weather",
            command=self._on_search_clicked
        )
        self.search_button.pack(side="left")
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press."""
        self._on_search_clicked()
    
    def _on_search_clicked(self):
        """Handle search button click."""
        city = self.city_entry.get().strip()
        if city:
            self.on_search(city)
        else:
            messagebox.showwarning("Input Error", "Please enter a city name.")
    
    def set_city(self, city: str):
        """Set city in the entry field."""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
    
    def clear(self):
        """Clear the search field."""
        self.city_entry.delete(0, tk.END)


class WeatherComparisonView:
    """View for weather comparison functionality."""
    
    def __init__(self, parent: tk.Widget, on_compare: Callable[[str, str], None]):
        self.parent = parent
        self.on_compare = on_compare
        self._create_widgets()
    
    def _create_widgets(self):
        """Create comparison widgets."""
        compare_frame = ttk.LabelFrame(self.parent, text="Compare Cities", padding="10")
        compare_frame.pack(fill="x", padx=10, pady=10)
        
        input_frame = ttk.Frame(compare_frame)
        input_frame.pack(fill="x")
        
        # City 1
        ttk.Label(input_frame, text="City 1:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.city1_entry = ttk.Entry(input_frame, width=20, font=("Arial", 12))
        self.city1_entry.grid(row=0, column=1, padx=(0, 20))
        
        # City 2
        ttk.Label(input_frame, text="City 2:").grid(row=0, column=2, sticky="w", padx=(0, 10))
        self.city2_entry = ttk.Entry(input_frame, width=20, font=("Arial", 12))
        self.city2_entry.grid(row=0, column=3, padx=(0, 20))
        
        # Compare button
        self.compare_button = ttk.Button(
            input_frame,
            text="Compare",
            command=self._on_compare_clicked
        )
        self.compare_button.grid(row=0, column=4)
        
        # Bind Enter key
        self.city1_entry.bind("<Return>", self._on_enter_pressed)
        self.city2_entry.bind("<Return>", self._on_enter_pressed)
    
    def _on_enter_pressed(self, event):
        """Handle Enter key press."""
        self._on_compare_clicked()
    
    def _on_compare_clicked(self):
        """Handle compare button click."""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if city1 and city2:
            self.on_compare(city1, city2)
        else:
            messagebox.showwarning("Input Error", "Please enter both city names.")
    
    def clear(self):
        """Clear both entry fields."""
        self.city1_entry.delete(0, tk.END)
        self.city2_entry.delete(0, tk.END)
