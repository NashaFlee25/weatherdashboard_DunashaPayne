"""
VibeCast Application

Tune in to your day's weather rhythm.

A modern, user-friendly weather dashboard that provides current weather information,
historical data tracking, and weather statistics with a clean GUI interface.

Requirements:
- Install requests: pip install requests
- Install python-dotenv: pip install python-dotenv
- Install matplotlib: pip install matplotlib
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import json
from dotenv import load_dotenv
from typing import List, Dict, Tuple
from datetime import datetime

# Define theme color schemes
THEME_SCHEMES = {
    "Blue": {"bg": "#ddefff", "fg": "#002244", "accent": "#6699cc"},
    "Green": {"bg": "#e8f5e9", "fg": "#1b5e20", "accent": "#66bb6a"},
    "Pink": {"bg": "#fce4ec", "fg": "#880e4f", "accent": "#ec407a"},
    "Dark": {"bg": "#303030", "fg": "#eeeeee", "accent": "#757575"},
    "Purple": {"bg": "#f3e5f5", "fg": "#4a148c", "accent": "#ab47bc"}
}

# Load environment variables from .env file
load_dotenv()

# Check if requests is installed before proceeding
try:
    import requests
except ImportError:
    print("Error: 'requests' library is not installed.")
    print("Please install it using: pip install requests")
    sys.exit(1)

# Check if matplotlib is installed before proceeding
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np
except ImportError:
    print("Error: 'matplotlib' library is not installed.")
    print("Please install it using: pip install matplotlib")
    sys.exit(1)

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if (project_root not in sys.path):
    sys.path.insert(0, project_root)

from features.tracker import (
    save_weather_to_csv,
    read_last_n_entries,
    calculate_stats_from_csv,
    get_weather_phrase,
    get_personalized_greeting
)


def get_emoji_font(size):
    """Get the appropriate emoji font for the current platform"""
    if sys.platform == "win32":
        return ("Segoe UI Emoji", size)
    elif sys.platform == "darwin":
        return ("Apple Color Emoji", size)
    else:
        return ("Noto Color Emoji", size)


class GUIIcons:
    """Weather condition code to icon mapping for GUI display"""

    @staticmethod
    def get_weather_icon(condition_code: int) -> str:
        """Map OpenWeatherMap condition codes to appropriate emoji icons"""
        # Thunderstorm
        if 200 <= condition_code <= 232:
            return "⛈️"
        # Drizzle
        elif 300 <= condition_code <= 321:
            return "🌦️"
        # Rain
        elif 500 <= condition_code <= 531:
            return "🌧️"
        # Snow
        elif 600 <= condition_code <= 622:
            return "❄️"
        # Atmosphere (mist, fog, etc.)
        elif 701 <= condition_code <= 781:
            return "🌫️"
        # Clear
        elif condition_code == 800:
            return "☀️"
        # Clouds
        elif 801 <= condition_code <= 804:
            if condition_code == 801:
                return "🌤️"  # Few clouds
            elif condition_code == 802:
                return "⛅"   # Scattered clouds
            else:
                return "☁️"   # Broken/overcast clouds
        else:
            return "🌤️"  # Default


class WeatherService:
    def __init__(self):
        # Get API key from environment variable loaded from .env file
        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY not found in environment variables. Please check your .env file.")

    def get_weather(self, city: str) -> dict:
        """
        Get weather data for a given city from OpenWeatherMap API.

        Args:
            city: Name of the city to get weather for

        Returns:
            Dictionary containing weather data

        Raises:
            Exception: If API call fails or data parsing fails
        """
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": self.api_key, "units": "metric"}

            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            # Parse the response data
            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"]
            }

            return weather_data

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 404:
                raise Exception(f"City '{city}' not found")
            elif resp.status_code == 401:
                raise Exception("Invalid API key")
            else:
                raise Exception(f"HTTP error: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: missing {e}")
        except Exception as e:
            raise Exception(f"Failed to get weather data: {e}")

    def get_5_day_forecast(self, city: str) -> List[Dict]:
        """
        Get 5-day weather forecast for a given city from OpenWeatherMap API.

        Args:
            city: Name of the city to get forecast for

        Returns:
            List of dictionaries containing forecast data for 5 days

        Raises:
            Exception: If API call fails or data parsing fails
        """
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": self.api_key, "units": "metric"}

            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            forecast_list = []
            processed_dates = set()

            # Process forecast data (API returns 40 entries for 5 days, every 3 hours)
            for item in data["list"]:
                # Convert timestamp to date
                forecast_date = datetime.fromtimestamp(item["dt"])
                date_key = forecast_date.strftime("%Y-%m-%d")

                # Skip if we already have data for this date
                if date_key in processed_dates:
                    continue

                # Take the first forecast of each day (usually around midnight or early morning)
                # This gives us one forecast per day for 5 days
                forecast_entry = {
                    "date": forecast_date.strftime("%a %b %d"),  # e.g., "Tue Aug 5"
                    "temp": round(item["main"]["temp"]),
                    "condition_code": item["weather"][0]["id"],
                    "description": item["weather"][0]["description"]
                }

                forecast_list.append(forecast_entry)
                processed_dates.add(date_key)

                # Stop when we have 5 days
                if len(forecast_list) >= 5:
                    break

            return forecast_list

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 404:
                raise Exception(f"City '{city}' not found for forecast")
            elif resp.status_code == 401:
                raise Exception("Invalid API key for forecast")
            else:
                raise Exception(f"HTTP error in forecast: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error in forecast: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected forecast API response format: missing {e}")
        except Exception as e:
            raise Exception(f"Failed to get forecast data: {e}")

    def get_5_day_temperatures(self, city: str) -> List[Tuple[str, float]]:
        """
        Get 5-day temperature data for chart display.

        Args:
            city: Name of the city to get temperature data for

        Returns:
            List of tuples containing (date_string, temperature)

        Raises:
            Exception: If API call fails or data parsing fails
        """
        try:
            url = "https://api.openweathermap.org/data/2.5/forecast"
            params = {"q": city, "appid": self.api_key, "units": "metric"}

            resp = requests.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()

            temperature_data = []
            processed_dates = set()

            # Process forecast data to get one temperature per day (midday preference)
            for item in data["list"]:
                forecast_datetime = datetime.fromtimestamp(item["dt"])
                date_key = forecast_datetime.strftime("%Y-%m-%d")

                # Skip if we already have data for this date
                if date_key in processed_dates:
                    continue

                # Format date for display (short format)
                date_str = forecast_datetime.strftime("%m/%d")
                temperature = round(item["main"]["temp"], 1)

                temperature_data.append((date_str, temperature))
                processed_dates.add(date_key)

                # Stop when we have 5 days
                if len(temperature_data) >= 5:
                    break

            return temperature_data

        except requests.exceptions.HTTPError as e:
            if resp.status_code == 404:
                raise Exception(f"City '{city}' not found for temperature data")
            elif resp.status_code == 401:
                raise Exception("Invalid API key for temperature data")
            else:
                raise Exception(f"HTTP error in temperature data: {e}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error in temperature data: {e}")
        except KeyError as e:
            raise Exception(f"Unexpected temperature API response format: missing {e}")
        except Exception as e:
            raise Exception(f"Failed to get temperature data: {e}")

    def get_temperature_comparison(self, city1: str, city2: str) -> Tuple[List[str], List[float], List[float]]:
        """
        Get temperature comparison data for two cities.

        Args:
            city1: Name of the first city
            city2: Name of the second city

        Returns:
            Tuple containing (dates, temps1, temps2)

        Raises:
            Exception: If API call fails for either city
        """
        try:
            # Get temperature data for both cities
            temps1_data = self.get_5_day_temperatures(city1)
            temps2_data = self.get_5_day_temperatures(city2)

            # Extract dates and temperatures
            dates1, temps1 = zip(*temps1_data) if temps1_data else ([], [])
            dates2, temps2 = zip(*temps2_data) if temps2_data else ([], [])

            # Use the common dates (should be the same for both cities)
            # If different lengths, use the shorter one
            min_length = min(len(dates1), len(dates2))
            dates = list(dates1[:min_length])
            temps1_list = list(temps1[:min_length])
            temps2_list = list(temps2[:min_length])

            return dates, temps1_list, temps2_list

        except Exception as e:
            raise Exception(f"Failed to get comparison data: {str(e)}")


class SettingsManager:
    def __init__(self):
        self._config_path = os.path.join(os.path.dirname(__file__), "settings.json")
        if os.path.exists(self._config_path):
            with open(self._config_path) as f:
                self._config = json.load(f)
        else:
            self._config = {}

    def get_last_city(self) -> str:
        return self._config.get("last_city", "")

    def save_last_city(self, city: str) -> None:
        self._config["last_city"] = city
        with open(self._config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    def get_last_name(self) -> str:
        return self._config.get("user_name", "")

    def save_last_name(self, name: str) -> None:
        self._config["user_name"] = name
        with open(self._config_path, "w") as f:
            json.dump(self._config, f, indent=2)

    def get_available_themes(self) -> List[str]:
        """Return list of available theme names"""
        return list(THEME_SCHEMES.keys())

    def load_theme(self) -> str:
        """Load saved theme or return default"""
        return self._config.get("theme", "Blue")

    def save_theme(self, theme_name: str) -> None:
        """Save selected theme to settings"""
        if theme_name in THEME_SCHEMES:
            self._config["theme"] = theme_name
            with open(self._config_path, "w") as f:
                json.dump(self._config, f, indent=2)

    def get_theme(self) -> str:
        return self.load_theme()


class WeatherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("VibeCast 🌦️")
        self.root.geometry("900x700")  # Increased width for tabbed interface

        # Initialize services
        self.weather_service = WeatherService()
        self.settings_manager = SettingsManager()

        # Load saved city
        self.current_city = self.settings_manager.get_last_city()

        # Initialize theme - load saved theme
        self.current_theme = self.settings_manager.load_theme()
        self.theme_var = tk.StringVar(value=self.current_theme)

        # Load available cities from CSV
        self.available_cities = self.load_cities_from_csv()

        # Initialize forecast variables
        self.forecast_vars = []

        # Initialize chart variables
        self.chart_canvas = None
        self.comparison_canvas = None

        # Setup GUI
        self.setup_gui()
        
        # Apply saved theme on startup
        self.apply_theme(self.current_theme)

        # Load saved name
        last_name = self.settings_manager.get_last_name()
        if last_name:
            self.name_entry.insert(0, last_name)

        # Load weather for saved city if exists
        if self.current_city:
            self.city_entry.insert(0, self.current_city)
            self.get_weather()

    def load_cities_from_csv(self):
        """Load available cities from the team CSV file"""
        try:
            from pathlib import Path
            import csv
            csv_path = Path(__file__).parent / "data" / "team_weather_data.csv"
            available_cities = set()

            with csv_path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    city = row.get("city", "").strip()
                    # Only include cities that have temperature data
                    if city and any(row.get(col, "").strip() for col in ["temperature", "temp_f"]):
                        # Check if the temperature and humidity values are not empty or zero
                        temp_str = ""
                        hum_str = ""

                        for temp_col in ["temperature", "temp", "temp_f"]:
                            val = row.get(temp_col, "").strip()
                            if val and val != "0" and val != "0.0":
                                temp_str = val
                                break

                        for hum_col in ["humidity", "humidity_pct"]:
                            val = row.get(hum_col, "").strip()
                            if val and val != "0" and val != "0.0":
                                hum_str = val
                                break

                        if temp_str and hum_str:
                            available_cities.add(city)

            return sorted(list(available_cities))
        except Exception as e:
            print(f"Error loading cities from CSV: {e}")
            return []

    def setup_gui(self):
        # Main container frame
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill='both', expand=True)

        # Title and input section (always visible at top)
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill='x', pady=(0, 10))

        # Top row with title and theme selector
        title_row = ttk.Frame(header_frame)
        title_row.pack(fill='x', pady=(0, 10))

        # Title (left side)
        title_label = ttk.Label(title_row, text="VibeCast 🌦️",
                                font=("Arial", 24, "bold"))
        title_label.pack(side='left')

        # Theme controls (right side of title row)
        theme_frame = ttk.Frame(title_row)
        theme_frame.pack(side='right', padx=(10, 0))
        
        ttk.Label(theme_frame, text="Theme:", font=("Arial", 12)).pack(side='left', padx=(0, 5))
        self.theme_dropdown = ttk.Combobox(theme_frame, 
                                           textvariable=self.theme_var,
                                           values=self.settings_manager.get_available_themes(),
                                           state="readonly", 
                                           width=12,
                                           font=("Arial", 11))
        self.theme_dropdown.pack(side='left')
        self.theme_dropdown.bind('<<ComboboxSelected>>', self.on_theme_change)

        # Input frame
        input_frame = ttk.Frame(header_frame)
        input_frame.pack(fill='x', pady=(0, 10))

        # Name input
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill='x', pady=(0, 5))
        ttk.Label(name_frame, text="Name: 📝").pack(side='left', padx=(0, 10))
        self.name_entry = ttk.Entry(name_frame, font=("Arial", 12))
        self.name_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        # City input
        city_frame = ttk.Frame(input_frame)
        city_frame.pack(fill='x')
        ttk.Label(city_frame, text="City: 📍").pack(side='left', padx=(0, 10))
        self.city_entry = ttk.Entry(city_frame, font=("Arial", 12))
        self.city_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.get_weather())

        self.get_weather_btn = ttk.Button(city_frame, text="Get Weather 🌤️",
                                          command=self.get_weather)
        self.get_weather_btn.pack(side='right')

        # Greeting label
        self.greeting_label = ttk.Label(header_frame, text="", font=("Arial", 14, "italic"))
        self.greeting_label.pack(pady=(5, 0))

        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True, pady=(10, 0))

        # Create tab frames
        self.current_frame = ttk.Frame(self.notebook)
        self.forecast_frame = ttk.Frame(self.notebook)
        self.chart_frame = ttk.Frame(self.notebook)
        self.comparison_frame = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.current_frame, text="Current Weather")
        self.notebook.add(self.forecast_frame, text="5-Day Forecast")
        self.notebook.add(self.chart_frame, text="Temp Trend")
        self.notebook.add(self.comparison_frame, text="City Comparison")

        # Setup each tab
        self.setup_current_weather_tab()
        self.setup_forecast_tab()
        self.setup_chart_tab()
        self.setup_comparison_tab()

        # Control buttons at bottom
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill='x', pady=(10, 0))

        self.history_btn = ttk.Button(control_frame, text="View History 📜",
                                      command=self.show_history)
        self.history_btn.pack(side='left', padx=(0, 10))

        self.stats_btn = ttk.Button(control_frame, text="Weather Stats 📊",
                                    command=self.display_stats)
        self.stats_btn.pack(side='left', padx=(0, 10))

        # Add theme toggle button as backup option
        self.theme_toggle_btn = ttk.Button(control_frame, text="🎨 Toggle Theme",
                                           command=self.toggle_theme)
        self.theme_toggle_btn.pack(side='right', padx=(10, 0))

    def setup_current_weather_tab(self):
        """Setup the current weather tab"""
        # Weather display frame
        self.weather_frame = ttk.LabelFrame(self.current_frame, text="Current Weather ☀️", padding="20")
        self.weather_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Weather info labels
        self.city_label = ttk.Label(self.weather_frame, text="", font=("Arial", 18, "bold"))
        self.city_label.pack(pady=(0, 15))

        self.temp_label = ttk.Label(self.weather_frame, text="", font=("Arial", 16))
        self.temp_label.pack(pady=(0, 10))

        self.desc_label = ttk.Label(self.weather_frame, text="", font=("Arial", 14))
        self.desc_label.pack(pady=(0, 10))

        self.feels_like_label = ttk.Label(self.weather_frame, text="", font=("Arial", 12))
        self.feels_like_label.pack(pady=(0, 5))

        self.humidity_label = ttk.Label(self.weather_frame, text="", font=("Arial", 12))
        self.humidity_label.pack(pady=(0, 5))

        self.pressure_label = ttk.Label(self.weather_frame, text="", font=("Arial", 12))
        self.pressure_label.pack(pady=(0, 15))

        # Weather phrase with emoji support
        self.phrase_label = ttk.Label(self.weather_frame, text="", font=get_emoji_font(13))
        self.phrase_label.pack(pady=(0, 10))

    def setup_forecast_tab(self):
        """Setup the 5-day forecast tab"""
        # Forecast display frame
        forecast_display_frame = ttk.LabelFrame(self.forecast_frame, text="5-Day Weather Forecast 📅", padding="20")
        forecast_display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Create forecast display container
        self.forecast_container = ttk.Frame(forecast_display_frame)
        self.forecast_container.pack(expand=True)

        # Initialize forecast display
        self.setup_forecast_display()

    def setup_chart_tab(self):
        """Setup the temperature trend chart tab"""
        # Chart display frame
        chart_display_frame = ttk.LabelFrame(self.chart_frame, text="5-Day Temperature Trend 📊", padding="20")
        chart_display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Chart container
        self.chart_container = ttk.Frame(chart_display_frame)
        self.chart_container.pack(fill='both', expand=True)

    def setup_comparison_tab(self):
        """Setup the city comparison tab"""
        # Configure grid weights for proper resizing
        self.comparison_frame.columnconfigure(0, weight=1)
        self.comparison_frame.columnconfigure(1, weight=1)
        self.comparison_frame.columnconfigure(2, weight=1)
        self.comparison_frame.columnconfigure(3, weight=1)
        self.comparison_frame.columnconfigure(4, weight=0)
        self.comparison_frame.rowconfigure(1, weight=1)

        # Input controls frame
        input_controls_frame = ttk.LabelFrame(self.comparison_frame, text="Compare Cities 🏙️", padding="15")
        input_controls_frame.grid(row=0, column=0, columnspan=5, sticky="ew", padx=10, pady=10)

        # Configure input frame grid
        input_controls_frame.columnconfigure(1, weight=1)
        input_controls_frame.columnconfigure(3, weight=1)

        # City 1 dropdown
        ttk.Label(input_controls_frame, text="City 1:", font=("Arial", 12)).grid(row=0, column=0, padx=(0, 10), pady=5)
        self.city1_var = tk.StringVar()
        self.city1_dropdown = ttk.Combobox(input_controls_frame, textvariable=self.city1_var,
                                          values=self.available_cities, state="readonly", 
                                          font=("Arial", 12), width=20)
        self.city1_dropdown.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=5)

        # City 2 dropdown
        ttk.Label(input_controls_frame, text="City 2:", font=("Arial", 12)).grid(row=0, column=2, padx=(0, 10), pady=5)
        self.city2_var = tk.StringVar()
        self.city2_dropdown = ttk.Combobox(input_controls_frame, textvariable=self.city2_var,
                                          values=self.available_cities, state="readonly", 
                                          font=("Arial", 12), width=20)
        self.city2_dropdown.grid(row=0, column=3, sticky="ew", padx=(0, 20), pady=5)

        # Compare button
        self.compare_btn = ttk.Button(input_controls_frame, text="Compare 📊", command=self.compare_cities)
        self.compare_btn.grid(row=0, column=4, pady=5)

        # Bind selection events to both dropdowns
        self.city1_dropdown.bind('<<ComboboxSelected>>', lambda e: self.on_city_selection())
        self.city2_dropdown.bind('<<ComboboxSelected>>', lambda e: self.on_city_selection())

        # Chart display area
        self.comparison_chart_frame = ttk.LabelFrame(self.comparison_frame, text="Temperature Comparison Chart 📈", padding="15")
        self.comparison_chart_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=10, pady=(0, 10))
        self.comparison_chart_frame.columnconfigure(0, weight=1)
        self.comparison_chart_frame.rowconfigure(0, weight=1)

        # Initial placeholder
        placeholder_label = ttk.Label(self.comparison_chart_frame, 
                                     text="Select two cities from the dropdowns above and click 'Compare' to see\ntheir 5-day temperature comparison chart.",
                                     font=("Arial", 14),
                                     justify='center')
        placeholder_label.grid(row=0, column=0, sticky="nsew")

    def on_city_selection(self):
        """Handle city selection in dropdown - enable compare button when both cities are selected"""
        city1 = self.city1_var.get().strip()
        city2 = self.city2_var.get().strip()
        
        # Enable compare button only when both cities are selected and different
        if city1 and city2 and city1.lower() != city2.lower():
            self.compare_btn.config(state="normal")
        else:
            self.compare_btn.config(state="disabled")

    def compare_cities(self):
        """Compare temperature data between two cities"""
        city1 = self.city1_var.get().strip()
        city2 = self.city2_var.get().strip()

        # Validate input
        if not city1 or not city2:
            messagebox.showwarning("Warning", "Please select both cities from the dropdowns")
            return

        if city1.lower() == city2.lower():
            messagebox.showwarning("Warning", "Please select two different cities")
            return

        try:
            # Get comparison data
            dates, temps1, temps2 = self.weather_service.get_temperature_comparison(city1, city2)
            
            if not dates or not temps1 or not temps2:
                messagebox.showerror("Error", "Unable to get temperature data for comparison")
                return

            # Draw comparison chart
            self.draw_comparison_chart(dates, temps1, temps2, city1, city2)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self.clear_comparison_chart()

    def setup_forecast_display(self):
        """Initialize the 5-day forecast display with empty StringVars"""
        self.forecast_vars = []

        # Create 5 forecast day frames in a horizontal layout
        for i in range(5):
            day_frame = ttk.Frame(self.forecast_container)
            day_frame.grid(row=0, column=i, padx=15, pady=10)

            # StringVars for dynamic updates
            date_var = tk.StringVar(value="")
            temp_var = tk.StringVar(value="")
            icon_var = tk.StringVar(value="")

            # Labels for each day
            date_label = ttk.Label(day_frame, textvariable=date_var, font=("Arial", 12, "bold"))
            date_label.grid(row=0, column=0, pady=(0, 10))

            icon_label = ttk.Label(day_frame, textvariable=icon_var, font=get_emoji_font(32))
            icon_label.grid(row=1, column=0, pady=(0, 10))

            temp_label = ttk.Label(day_frame, textvariable=temp_var, font=("Arial", 13))
            temp_label.grid(row=2, column=0)

            # Store StringVars for updates
            self.forecast_vars.append({
                'date': date_var,
                'temp': temp_var,
                'icon': icon_var
            })

    def draw_temperature_chart(self, data: List[Tuple[str, float]]):
        """
        Draw a bar chart showing 5-day temperature trends in the chart tab.

        Args:
            data: List of tuples containing (date_string, temperature)
        """
        try:
            # Clear existing chart
            for widget in self.chart_container.winfo_children():
                widget.destroy()

            if not data:
                # Show empty chart message
                empty_label = ttk.Label(self.chart_container, text="No temperature data available", 
                                       font=("Arial", 14))
                empty_label.pack(expand=True)
                return

            # Create matplotlib figure
            fig = Figure(figsize=(8, 5), dpi=80)
            ax = fig.add_subplot(111)

            # Unpack data
            dates, temps = zip(*data)

            # Create bar chart
            bars = ax.bar(dates, temps, color='lightblue', edgecolor='darkblue', alpha=0.8, width=0.6)

            # Customize chart
            ax.set_title("5-Day Temperature Trend", fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel("Temperature (°C)", fontsize=14)
            ax.tick_params(axis='x', rotation=0, labelsize=12)
            ax.tick_params(axis='y', labelsize=12)
            ax.grid(True, alpha=0.3, axis='y')

            # Add temperature labels on bars
            for bar, temp in zip(bars, temps):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                       f'{temp}°C', ha='center', va='bottom', fontsize=11, fontweight='bold')

            # Set y-axis limits for better visibility
            if temps:
                min_temp = min(temps)
                max_temp = max(temps)
                temp_range = max_temp - min_temp
                padding = max(temp_range * 0.2, 3)
                ax.set_ylim(min_temp - padding, max_temp + padding)

            # Adjust layout
            fig.tight_layout(pad=2.0)

            # Create canvas and add to chart container
            self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            # Handle chart drawing errors
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            error_label = ttk.Label(self.chart_container, 
                                   text=f"Chart Error: {str(e)}", 
                                   font=("Arial", 12),
                                   foreground="red")
            error_label.pack(expand=True)
            print(f"Error drawing temperature chart: {e}")

    def draw_comparison_chart(self, dates: List[str], temps1: List[float], temps2: List[float], label1: str, label2: str):
        """
        Draw a side-by-side bar chart comparing temperatures between two cities.

        Args:
            dates: List of date strings
            temps1: List of temperatures for city 1
            temps2: List of temperatures for city 2
            label1: Name of city 1
            label2: Name of city 2
        """
        try:
            # Clear existing chart
            for widget in self.comparison_chart_frame.winfo_children():
                widget.destroy()

            if not dates or not temps1 or not temps2:
                # Show empty chart message
                empty_label = ttk.Label(self.comparison_chart_frame, 
                                       text="No comparison data available", 
                                       font=("Arial", 14))
                empty_label.grid(row=0, column=0, sticky="nsew")
                return

            # Create matplotlib figure
            fig = Figure(figsize=(10, 6), dpi=80)
            ax = fig.add_subplot(111)

            # Set up bar positions
            x = np.arange(len(dates))
            width = 0.35

            # Create side-by-side bars
            bars1 = ax.bar(x - width/2, temps1, width, label=label1, color='lightblue', alpha=0.8, edgecolor='darkblue')
            bars2 = ax.bar(x + width/2, temps2, width, label=label2, color='lightcoral', alpha=0.8, edgecolor='darkred')

            # Customize chart
            ax.set_title(f"5-Day Temperature Comparison: {label1} vs {label2}", fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel("Temperature (°C)", fontsize=14)
            ax.set_xlabel("Date", fontsize=14)
            ax.set_xticks(x)
            ax.set_xticklabels(dates, rotation=45, ha='right')
            ax.legend(fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')

            # Add temperature labels on bars
            for bars, temps in [(bars1, temps1), (bars2, temps2)]:
                for bar, temp in zip(bars, temps):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                           f'{temp}°C', ha='center', va='bottom', fontsize=10, fontweight='bold')

            # Set y-axis limits for better visibility
            all_temps = temps1 + temps2
            if all_temps:
                min_temp = min(all_temps)
                max_temp = max(all_temps)
                temp_range = max_temp - min_temp
                padding = max(temp_range * 0.15, 3)
                ax.set_ylim(min_temp - padding, max_temp + padding)

            # Adjust layout to prevent clipping
            fig.tight_layout()

            # Create canvas and add to comparison frame
            self.comparison_canvas = FigureCanvasTkAgg(fig, master=self.comparison_chart_frame)
            self.comparison_canvas.draw()
            self.comparison_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

            print(f"Comparison chart drawn successfully for {label1} vs {label2}")  # Debug info

        except Exception as e:
            # Handle chart drawing errors
            for widget in self.comparison_chart_frame.winfo_children():
                widget.destroy()
            error_label = ttk.Label(self.comparison_chart_frame, 
                                   text=f"Chart Error: {str(e)}", 
                                   font=("Arial", 12),
                                   foreground="red")
            error_label.grid(row=0, column=0, sticky="nsew")
            print(f"Error drawing comparison chart: {e}")

    def clear_temperature_chart(self):
        """Clear the temperature chart display"""
        try:
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            self.chart_canvas = None
        except Exception as e:
            print(f"Error clearing chart: {e}")

    def clear_comparison_chart(self):
        """Clear the comparison chart display"""
        try:
            for widget in self.comparison_chart_frame.winfo_children():
                widget.destroy()
            self.comparison_canvas = None
            
            # Show placeholder again
            placeholder_label = ttk.Label(self.comparison_chart_frame, 
                                         text="Select two cities from the dropdowns above and click 'Compare' to see\ntheir 5-day temperature comparison chart.",
                                         font=("Arial", 14),
                                         justify='center')
            placeholder_label.grid(row=0, column=0, sticky="nsew")
        except Exception as e:
            print(f"Error clearing comparison chart: {e}")

    def apply_theme(self, theme_name: str = None):
        """Apply the chosen theme colors to the window and all widgets."""
        if theme_name is None:
            theme_name = self.current_theme

        if theme_name not in THEME_SCHEMES:
            theme_name = "Blue"  # Default fallback

        scheme = THEME_SCHEMES[theme_name]
        bg, fg, accent = scheme["bg"], scheme["fg"], scheme["accent"]

        # Configure root window
        self.root.configure(bg=bg)

        # Configure ttk Style
        style = ttk.Style()
        
        if theme_name == "Dark":
            style.theme_use("clam")
            style.configure(".", background=bg, foreground=fg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TFrame", background=bg)
            style.configure("TLabelFrame", background=bg, foreground=fg)
            style.configure("TButton", background=accent, foreground=fg)
            style.configure("TCombobox",
                            foreground=fg,
                            fieldbackground=accent,
                            background=bg,
                            selectbackground=accent,
                            selectforeground=fg)
            style.configure("TEntry",
                            foreground=fg,
                            fieldbackground=accent,
                            background=bg)
            style.configure("Treeview", background=accent, foreground=fg)
            style.configure("Treeview.Heading", background=bg, foreground=fg)
            style.configure("TNotebook", background=bg)
            style.configure("TNotebook.Tab", background=accent, foreground=fg)
        else:
            # For Light themes (Blue, Green, Pink, Purple)
            style.theme_use("default")
            style.configure(".", background=bg, foreground=fg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TFrame", background=bg)
            style.configure("TLabelFrame", background=bg, foreground=fg)
            style.configure("TButton", background=accent, foreground="white")
            style.configure("TCombobox", 
                            background=bg, 
                            foreground=fg,
                            fieldbackground="white",
                            selectbackground=accent,
                            selectforeground="white")
            style.configure("TEntry", 
                            background=bg, 
                            foreground=fg,
                            fieldbackground="white")
            style.configure("Treeview", background="white", foreground=fg)
            style.configure("Treeview.Heading", background=accent, foreground="white")
            style.configure("TNotebook", background=bg)
            style.configure("TNotebook.Tab", background=accent, foreground="white")

        self.current_theme = theme_name
        
        # Update the dropdown to show current theme
        self.theme_var.set(theme_name)

    def on_theme_change(self, event=None):
        """Handle theme change from dropdown"""
        theme = self.theme_var.get()
        self.apply_theme(theme)
        self.settings_manager.save_theme(theme)

    def toggle_theme(self):
        """Toggle between themes (cycling through all available themes)"""
        themes = self.settings_manager.get_available_themes()
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        next_theme = themes[next_index]
        self.theme_var.set(next_theme)
        self.apply_theme(next_theme)
        self.settings_manager.save_theme(next_theme)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return

        # Save name and show greeting
        name = self.name_entry.get().strip()
        if name:
            self.settings_manager.save_last_name(name)
            greeting = get_personalized_greeting(name)
            self.greeting_label.config(text=greeting)

        try:
            weather_data = self.weather_service.get_weather(city)
            if weather_data:
                self.display_weather(weather_data)
                # Save to CSV
                save_weather_to_csv(weather_data)
                # Save city to settings
                self.settings_manager.save_last_city(city)
                self.current_city = city

                # Get and display 5-day forecast
                try:
                    forecast_data = self.weather_service.get_5_day_forecast(city)
                    self.update_forecast_display(forecast_data)
                except Exception as forecast_error:
                    print(f"Forecast error: {forecast_error}")
                    self.display_forecast_error(str(forecast_error))

                # Get and display 5-day temperature chart
                try:
                    temp_data = self.weather_service.get_5_day_temperatures(city)
                    self.draw_temperature_chart(temp_data)
                except Exception as chart_error:
                    print(f"Temperature chart error: {chart_error}")
                    self.clear_temperature_chart()
            else:
                messagebox.showerror("Error", f"Weather data not found for {city}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")
            self.clear_forecast_display()
            self.clear_temperature_chart()

    def display_weather(self, weather_data):
        """Display weather data in the GUI"""
        self.city_label.config(text=f"{weather_data['city']}, {weather_data['country']}")
        self.temp_label.config(text=f"🌡️ Temperature: {weather_data['temperature']:.1f}°C")
        self.desc_label.config(text=f"🌦️ Condition: {weather_data['description'].title()}")
        self.feels_like_label.config(text=f"🤗 Feels like: {weather_data['feels_like']:.1f}°C")
        self.humidity_label.config(text=f"💧 Humidity: {weather_data['humidity']}%")
        self.pressure_label.config(text=f"🔽 Pressure: {weather_data['pressure']} hPa")

        # Display weather phrase with proper emoji font
        phrase = get_weather_phrase(weather_data['temperature'], weather_data['description'])
        self.phrase_label.config(text=phrase, font=get_emoji_font(11))

    def update_forecast_display(self, forecast_data: List[Dict]):
        """Update the forecast display with new data"""
        try:
            for i, day_data in enumerate(forecast_data[:5]):  # Ensure max 5 days
                if i < len(self.forecast_vars):
                    self.forecast_vars[i]['date'].set(day_data['date'])
                    self.forecast_vars[i]['temp'].set(f"{day_data['temp']}°C")
                    self.forecast_vars[i]['icon'].set(GUIIcons.get_weather_icon(day_data['condition_code']))

            # Clear remaining slots if less than 5 days
            for i in range(len(forecast_data), 5):
                if i < len(self.forecast_vars):
                    self.forecast_vars[i]['date'].set("")
                    self.forecast_vars[i]['temp'].set("")
                    self.forecast_vars[i]['icon'].set("")

        except Exception as e:
            # Handle any errors in display update
            self.clear_forecast_display()
            print(f"Error updating forecast display: {e}")

    def clear_forecast_display(self):
        """Clear the forecast display"""
        for forecast_var in self.forecast_vars:
            forecast_var['date'].set("")
            forecast_var['temp'].set("")
            forecast_var['icon'].set("")

    def display_forecast_error(self, error_message: str):
        """Display error message in forecast frame"""
        self.clear_forecast_display()
        # Show error in the first forecast slot
        if self.forecast_vars:
            self.forecast_vars[0]['date'].set("Forecast")
            self.forecast_vars[0]['temp'].set("Unavailable")
            self.forecast_vars[0]['icon'].set("❌")

    def show_history(self):
        """Show weather history in a new window"""
        try:
            history_data = read_last_n_entries(10)  # Get last 10 entries
            if not history_data:
                messagebox.showinfo("History", "No weather history available")
                return

            # Create history window
            history_window = tk.Toplevel(self.root)
            history_window.title("Weather History 📜")
            history_window.geometry("900x500")

            # Create treeview for history
            columns = ("Timestamp", "City", "Temperature", "Description", "Humidity", "Pressure")
            tree = ttk.Treeview(history_window, columns=columns, show="headings", height=15)

            # Configure columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=140, anchor="center")

            # Add scrollbar
            scrollbar = ttk.Scrollbar(history_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Pack widgets
            tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
            scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

            # Insert data
            for entry in history_data:
                tree.insert("", "end", values=(
                    entry['timestamp'],
                    f"{entry['city']}, {entry['country']}",
                    f"{float(entry['temperature']):.1f}°C",
                    entry['description'].title(),
                    f"{int(entry['humidity'])}%",
                    f"{int(entry['pressure'])} hPa"
                ))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load history: {str(e)}")

    def display_stats(self):
        """Display weather statistics in a new window"""
        try:
            stats = calculate_stats_from_csv()
            if not stats:
                messagebox.showinfo("Statistics", "No weather data available for statistics")
                return

            # Create stats window
            stats_window = tk.Toplevel(self.root)
            stats_window.title("Weather Statistics 📈")
            stats_window.geometry("500x400")

            # Main frame
            main_frame = ttk.Frame(stats_window, padding="20")
            main_frame.pack(fill="both", expand=True)

            # Title
            title_label = ttk.Label(main_frame, text="Weather Statistics 📈",
                                    font=("Arial", 16, "bold"))
            title_label.pack(pady=(0, 20))

            # Stats frame
            stats_frame = ttk.LabelFrame(main_frame, text="Temperature Statistics", padding="15")
            stats_frame.pack(fill="x", pady=(0, 10))

            ttk.Label(stats_frame, text=f"Average Temperature: {stats['avg_temp']:.1f}°C",
                      font=("Arial", 12)).pack(anchor="w", pady=2)
            ttk.Label(stats_frame, text=f"Highest Temperature: {stats['max_temp']:.1f}°C",
                      font=("Arial", 12)).pack(anchor="w", pady=2)
            ttk.Label(stats_frame, text=f"Lowest Temperature: {stats['min_temp']:.1f}°C",
                      font=("Arial", 12)).pack(anchor="w", pady=2)

            # Cities frame
            cities_frame = ttk.LabelFrame(main_frame, text="Most Searched Cities", padding="15")
            cities_frame.pack(fill="x", pady=(0, 10))

            for i, (city, count) in enumerate(stats['top_cities'][:5], 1):
                ttk.Label(cities_frame, text=f"{i}. {city}: {count} searches",
                          font=("Arial", 11)).pack(anchor="w", pady=1)

            # General stats frame
            general_frame = ttk.LabelFrame(main_frame, text="General Statistics", padding="15")
            general_frame.pack(fill="x")

            ttk.Label(general_frame, text=f"Total Searches: {stats['total_searches']}",
                      font=("Arial", 12)).pack(anchor="w", pady=2)
            ttk.Label(general_frame, text=f"Average Humidity: {stats['avg_humidity']:.1f}%",
                      font=("Arial", 12)).pack(anchor="w", pady=2)
            ttk.Label(general_frame, text=f"Average Pressure: {stats['avg_pressure']:.1f} hPa",
                      font=("Arial", 12)).pack(anchor="w", pady=2)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load statistics: {str(e)}")


def main():
    # Create and run the application
    root = tk.Tk()
    app = WeatherDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()

