import tkinter as tk
from tkinter import messagebox

from src.services.weather_service import WeatherService
from src.config.settings_manager import SettingsManager
from features.tracker import save_weather_to_csv
from gui_icons import GUIIcons



class WeatherDashboard:
    """
    Weather Dashboard GUI application using Tkinter.
    """
    WINDOW_TITLE = "Weather Dashboard"
    WINDOW_SIZE = "500x300"

    def __init__(self):
        self.weather_service = WeatherService()
        self.settings = SettingsManager()
        self.root = tk.Tk()
        self.result_text = tk.StringVar()
        self.icon_text = tk.StringVar()
        self._setup_gui()

    def _setup_gui(self):
        """Set up the main GUI components."""
        self.root.title(self.WINDOW_TITLE)
        self.root.geometry(self.WINDOW_SIZE)

        tk.Label(self.root, text="Enter City Name:").grid(row=0, column=0, padx=10, pady=10)
        self.city_entry = tk.Entry(self.root, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Get Weather", command=self.display_weather).grid(row=1, column=0, columnspan=2, pady=10)

        # Weather icon label
        self.icon_label = tk.Label(self.root, textvariable=self.icon_text, font=("Arial", 32))
        self.icon_label.grid(row=2, column=0, padx=10, pady=10)

        tk.Label(self.root, textvariable=self.result_text, justify="left", wraplength=400).grid(row=2, column=1, padx=10, pady=10)

        last_city = self.settings.get_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def display_weather(self):
        """Fetch and display weather data for the entered city."""
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        try:
            weather_data = self.weather_service.get_weather_data(city_name)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

        if weather_data:
            self.settings.set_last_city(city_name)
            self._update_display(weather_data)
        else:
            messagebox.showerror("Error", "Could not fetch weather data. Please try again.")

    def _update_display(self, weather_data):
        """Update the result label, weather icon, and save weather data to CSV."""
        # Get icon for current weather
        icon = GUIIcons.get_icon(weather_data.get('description', ''), weather_data.get('temperature'))
        self.icon_text.set(icon)
        self.result_text.set(
            f"Weather in {weather_data['city']}:\n"
            f"Temperature: {weather_data['temperature']}°C\n"
            f"Description: {weather_data['description']}\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Wind Speed: {weather_data['wind_speed']} m/s"
        )
        try:
            save_weather_to_csv(
                weather_data['city'],
                weather_data['temperature'],
                weather_data['description']
            )
            messagebox.showinfo("Success", "Weather data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save weather data: {e}")

    def _on_close(self):
        """Handle application close event."""
        self.root.destroy()



def main():
    """Main entry point for the Weather Dashboard app."""
    app = WeatherDashboard()
    app.root.mainloop()

if __name__ == "__main__":
    main()
