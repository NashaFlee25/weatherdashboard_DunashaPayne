"""
Weather Dashboard Application

A modern, user-friendly weather dashboard that provides current weather information,
historical data tracking, and weather statistics with a clean GUI interface.

Requirements:
- Install requests: pip install requests
- Install python-dotenv: pip install python-dotenv
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if requests is installed before proceeding
try:
    import requests
except ImportError:
    print("Error: 'requests' library is not installed.")
    print("Please install it using: pip install requests")
    sys.exit(1)

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from features.tracker import (
    save_weather_to_csv,
    read_last_n_entries,
    calculate_stats_from_csv,
    get_weather_phrase
)


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
    
    def get_theme(self) -> str:
        return self._config.get("theme", "light")
    
    def save_theme(self, theme: str) -> None:
        self._config["theme"] = theme
        with open(self._config_path, "w") as f:
            json.dump(self._config, f, indent=2)


class WeatherDashboard:
    # Add themes as class attribute
    THEMES = {
        "Light":   {"bg": "SystemButtonFace", "fg": "black"},
        "Dark":    {"bg": "#2b2b2b",         "fg": "white"},
        "Blue":    {"bg": "#ADD8E6",         "fg": "navy"},
        "Green":   {"bg": "#D0F0C0",         "fg": "darkgreen"},
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        
        # Initialize services
        self.weather_service = WeatherService()
        self.settings_manager = SettingsManager()
        
        # Load saved city
        self.current_city = self.settings_manager.get_last_city()
        
        # Initialize theme - use saved theme or default to Light
        saved_theme = self.settings_manager.get_theme()
        self.current_theme = saved_theme if saved_theme in self.THEMES else "Light"
        
        # Setup GUI
        self.setup_gui()
        self.apply_theme(self.current_theme)
        
        # Load weather for saved city if exists
        if self.current_city:
            self.city_entry.insert(0, self.current_city)
            self.get_weather()

    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Weather Dashboard", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # City input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="City:").grid(row=0, column=0, padx=(0, 10))
        self.city_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.city_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.city_entry.bind('<Return>', lambda e: self.get_weather())
        
        self.get_weather_btn = ttk.Button(input_frame, text="Get Weather", 
                                         command=self.get_weather)
        self.get_weather_btn.grid(row=0, column=2)
        
        # Weather display frame
        self.weather_frame = ttk.LabelFrame(main_frame, text="Current Weather", padding="15")
        self.weather_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), 
                               pady=(0, 20))
        self.weather_frame.columnconfigure(0, weight=1)
        
        # Weather info labels
        self.city_label = ttk.Label(self.weather_frame, text="", font=("Arial", 16, "bold"))
        self.city_label.grid(row=0, column=0, pady=(0, 10))
        
        self.temp_label = ttk.Label(self.weather_frame, text="", font=("Arial", 14))
        self.temp_label.grid(row=1, column=0, pady=(0, 5))
        
        self.desc_label = ttk.Label(self.weather_frame, text="", font=("Arial", 12))
        self.desc_label.grid(row=2, column=0, pady=(0, 5))
        
        self.feels_like_label = ttk.Label(self.weather_frame, text="", font=("Arial", 10))
        self.feels_like_label.grid(row=3, column=0, pady=(0, 5))
        
        self.humidity_label = ttk.Label(self.weather_frame, text="", font=("Arial", 10))
        self.humidity_label.grid(row=4, column=0, pady=(0, 5))
        
        self.pressure_label = ttk.Label(self.weather_frame, text="", font=("Arial", 10))
        self.pressure_label.grid(row=5, column=0, pady=(0, 10))
        
        # Weather phrase
        self.phrase_label = ttk.Label(self.weather_frame, text="", font=("Arial", 11, "italic"))
        self.phrase_label.grid(row=6, column=0, pady=(0, 5))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 20))
        
        self.history_btn = ttk.Button(button_frame, text="View History", 
                                     command=self.show_history)
        self.history_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stats_btn = ttk.Button(button_frame, text="Weather Stats", 
                                   command=self.display_stats)
        self.stats_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Theme dropdown
        ttk.Label(button_frame, text="Theme:").grid(row=0, column=2, padx=(10, 5))
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_dropdown = ttk.Combobox(button_frame, textvariable=self.theme_var,
                                          values=list(self.THEMES.keys()),
                                          state="readonly", width=10)
        self.theme_dropdown.grid(row=0, column=3, padx=(0, 10))
        self.theme_dropdown.bind('<<ComboboxSelected>>', self.on_theme_change)

    def apply_theme(self, selected_theme=None):
        """Apply the chosen theme colors to the window and all widgets."""
        if selected_theme is None:
            selected_theme = self.current_theme
            
        if selected_theme not in self.THEMES:
            selected_theme = "Light"
            
        style_config = self.THEMES[selected_theme]
        bg, fg = style_config["bg"], style_config["fg"]
        
        # Configure ttk Style
        style = ttk.Style()
        
        if selected_theme == "Dark":
            style.theme_use("clam")
            style.configure(".", background=bg, foreground=fg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("TFrame", background=bg)
            style.configure("TLabelFrame", background=bg, foreground=fg)
            style.configure("TButton", background="#404040", foreground=fg)
            style.configure("TCombobox", 
                          foreground=fg,
                          fieldbackground="#404040",
                          background="#404040")
            style.configure("TEntry", 
                          foreground=fg,
                          fieldbackground="#404040",
                          background="#404040")
        else:
            # For Light, Blue, and Green themes
            style.theme_use("default")
            if selected_theme != "Light":
                style.configure(".", background=bg, foreground=fg)
                style.configure("TLabel", background=bg, foreground=fg)
                style.configure("TFrame", background=bg)
                style.configure("TLabelFrame", background=bg, foreground=fg)
                style.configure("TButton", background=bg, foreground=fg)
                style.configure("TCombobox", background=bg, foreground=fg)
                style.configure("TEntry", background=bg, foreground=fg)
        
        # Configure root window
        self.root.configure(bg=bg)
        self.current_theme = selected_theme

    def on_theme_change(self, event=None):
        """Handle theme change from dropdown"""
        selected_theme = self.theme_var.get()
        self.apply_theme(selected_theme)
        self.settings_manager.save_theme(selected_theme)

    def toggle_theme(self):
        """Toggle between themes (kept for backward compatibility)"""
        current_index = list(self.THEMES.keys()).index(self.current_theme)
        next_index = (current_index + 1) % len(self.THEMES)
        next_theme = list(self.THEMES.keys())[next_index]
        self.theme_var.set(next_theme)
        self.apply_theme(next_theme)
        self.settings_manager.save_theme(next_theme)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        try:
            weather_data = self.weather_service.get_weather(city)
            if weather_data:
                self.display_weather(weather_data)
                # Save to CSV
                save_weather_to_csv(weather_data)
                # Save city to settings
                self.settings_manager.save_last_city(city)
                self.current_city = city
            else:
                messagebox.showerror("Error", f"Weather data not found for {city}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")

    def display_weather(self, weather_data):
        """Display weather data in the GUI"""
        self.city_label.config(text=f"{weather_data['city']}, {weather_data['country']}")
        self.temp_label.config(text=f"Temperature: {weather_data['temperature']:.1f}°C")
        self.desc_label.config(text=f"Condition: {weather_data['description'].title()}")
        self.feels_like_label.config(text=f"Feels like: {weather_data['feels_like']:.1f}°C")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        self.pressure_label.config(text=f"Pressure: {weather_data['pressure']} hPa")
        
        # Display weather phrase
        phrase = get_weather_phrase(weather_data['temperature'], weather_data['description'])
        self.phrase_label.config(text=phrase)

    def show_history(self):
        """Show weather history in a new window"""
        try:
            history_data = read_last_n_entries(10)  # Get last 10 entries
            if not history_data:
                messagebox.showinfo("History", "No weather history available")
                return
            
            # Create history window
            history_window = tk.Toplevel(self.root)
            history_window.title("Weather History")
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
            stats_window.title("Weather Statistics")
            stats_window.geometry("500x400")
            
            # Main frame
            main_frame = ttk.Frame(stats_window, padding="20")
            main_frame.pack(fill="both", expand=True)
            
            # Title
            title_label = ttk.Label(main_frame, text="Weather Statistics", 
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

