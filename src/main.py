"""Main entry point for Weather Dashboard Application."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Check for required dependencies before importing
try:
    import aiohttp
except ImportError:
    print("Error: Missing required dependency 'aiohttp'")
    print("Please install it using: pip install aiohttp")
    sys.exit(1)

try:
    from config import WeatherConfig
    from app.weather_service import WeatherService
    from features.city_comparison import CityComparison
    from features.weather_icons import WeatherIcons
    from features.theme_switcher import ThemeSwitcher
    from utils.dependencies import DependencyChecker
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all required modules are available.")
    sys.exit(1)


class WeatherDashboard:
    """Main Weather Dashboard Application."""
    
    def __init__(self):
        """Initialize the weather dashboard."""
        self.root = tk.Tk()
        self.root.title("Weather Dashboard - Dunasha Payne")
        self.root.geometry("800x600")
        
        # Initialize dependencies
        self.dep_checker = DependencyChecker()
        
        # Try to initialize config and check for API key
        try:
            self.config = WeatherConfig()
            self.weather_service = WeatherService(self.config)
        except Exception as e:
            if "API key not found" in str(e):
                self.handle_missing_api_key()
            else:
                messagebox.showerror("Configuration Error", f"Failed to initialize: {str(e)}")
                sys.exit(1)
        
        # Initialize features
        self.city_comparison = CityComparison(self.weather_service)
        self.weather_icons = WeatherIcons()
        self.theme_switcher = ThemeSwitcher(self.root)
        
        self.setup_ui()
        self.show_dependency_warnings()
    
    def handle_missing_api_key(self):
        """Handle missing API key by prompting user to configure it."""
        message = """OpenWeather API Key Required
        
To use this weather dashboard, you need a free API key from OpenWeatherMap.

Steps to get your API key:
1. Visit: https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key from your account dashboard

Would you like to enter your API key now?"""
        
        if messagebox.askyesno("API Key Required", message):
            self.prompt_for_api_key()
        else:
            messagebox.showinfo("Setup Required", 
                              "You can set the OPENWEATHER_API_KEY environment variable and restart the application.")
            sys.exit(0)
    
    def prompt_for_api_key(self):
        """Prompt user to enter API key."""
        api_key = simpledialog.askstring(
            "Enter API Key",
            "Please enter your OpenWeatherMap API key:",
            show='*'
        )
        
        if api_key and api_key.strip():
            # Set environment variable temporarily
            os.environ['OPENWEATHER_API_KEY'] = api_key.strip()
            
            # Try to reinitialize with the new API key
            try:
                self.config = WeatherConfig()
                self.weather_service = WeatherService(self.config)
                messagebox.showinfo("Success", "API key configured successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to configure API key: {str(e)}")
                sys.exit(1)
        else:
            messagebox.showwarning("Setup Required", 
                                 "API key is required to use the weather dashboard.")
            sys.exit(0)
    
    def setup_ui(self):
        """Setup the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Weather Dashboard", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # City input
        ttk.Label(main_frame, text="Enter City:").grid(row=1, column=0, sticky=tk.W)
        self.city_var = tk.StringVar()
        city_entry = ttk.Entry(main_frame, textvariable=self.city_var, width=20)
        city_entry.grid(row=1, column=1, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Get weather button
        get_weather_btn = ttk.Button(main_frame, text="Get Weather", 
                                    command=self.get_weather)
        get_weather_btn.grid(row=1, column=2, padx=(5, 0))
        
        # Weather display area
        self.weather_text = tk.Text(main_frame, height=15, width=60)
        self.weather_text.grid(row=2, column=0, columnspan=3, pady=(20, 0), 
                              sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for text area
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, 
                                 command=self.weather_text.yview)
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S))
        self.weather_text.configure(yscrollcommand=scrollbar.set)
        
        # Feature buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        # Compare cities button
        compare_btn = ttk.Button(button_frame, text="Compare Cities", 
                                command=self.open_city_comparison)
        compare_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Theme switcher button
        theme_btn = ttk.Button(button_frame, text="Switch Theme", 
                              command=self.theme_switcher.toggle_theme)
        theme_btn.grid(row=0, column=1, padx=5)
        
        # Settings button
        settings_btn = ttk.Button(button_frame, text="Settings", 
                                 command=self.open_settings)
        settings_btn.grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def open_settings(self):
        """Open settings dialog."""
        if messagebox.askyesno("Update API Key", "Would you like to update your API key?"):
            self.prompt_for_api_key()
    
    def get_weather(self):
        """Get weather for the entered city."""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name.")
            return
        
        try:
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                self.display_weather(weather_data)
            else:
                self.weather_text.delete(1.0, tk.END)
                self.weather_text.insert(tk.END, f"Could not retrieve weather data for {city}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")
    
    def display_weather(self, weather_data):
        """Display weather data in the text area."""
        self.weather_text.delete(1.0, tk.END)
        
        display_text = f"""Weather for {weather_data.get('city', 'Unknown')}
        
Temperature: {weather_data.get('temperature', 'N/A')}°C
Description: {weather_data.get('description', 'N/A')}
Humidity: {weather_data.get('humidity', 'N/A')}%
Wind Speed: {weather_data.get('wind_speed', 'N/A')} m/s
Pressure: {weather_data.get('pressure', 'N/A')} hPa
        
Last Updated: {weather_data.get('timestamp', 'N/A')}
"""
        
        self.weather_text.insert(tk.END, display_text)
    
    def open_city_comparison(self):
        """Open the city comparison window."""
        self.city_comparison.open_comparison_window()
    
    def show_dependency_warnings(self):
        """Show warnings for missing optional dependencies."""
        self.dep_checker.show_warnings()
    
    def run(self):
        """Start the application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")


def main():
    """Main function to start the application."""
    try:
        app = WeatherDashboard()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
