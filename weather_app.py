from weather_logger import log_weather_data
from settings_manager import SettingsManager

class WeatherApp:
    def __init__(self):
        self.settings = SettingsManager()
        
        # Load saved preferences
        last_city = self.settings.get_last_city()
        if last_city:
            self.search_city(last_city)
            
        saved_theme = self.settings.get_theme()
        self.apply_theme(saved_theme)

    def search_city(self, city=None):
        # ...existing code...
        self.settings.set_last_city(city)
        # ...existing code...

    def toggle_theme(self):
        # ...existing code...
        new_theme = "dark" if current_theme == "light" else "light"
        self.settings.set_theme(new_theme)
        # ...existing code...

    def apply_theme(self, theme):
        # ...existing code...

def get_weather():
    # ...existing code...
    if weather_data:
        # After successfully getting weather data and before updating the GUI
        log_weather_data(
            city=city_name,
            temp=weather_data['main']['temp'],
            description=weather_data['weather'][0]['description']
        )
    # ...existing code...
