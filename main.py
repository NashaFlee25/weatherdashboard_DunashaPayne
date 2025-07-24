import tkinter as tk
from tkinter import messagebox
from src.services.weather_service import WeatherService
from src.config.settings_manager import SettingsManager
from features.tracker import save_weather_to_csv


class WeatherDashboard:
    def __init__(self):
        self.weather_service = WeatherService()
        self.settings = SettingsManager()
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("500x300")

        tk.Label(self.root, text="Enter City Name:").grid(row=0, column=0, padx=10, pady=10)
        self.city_entry = tk.Entry(self.root, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Get Weather", command=self.display_weather).grid(row=1, column=0, columnspan=2, pady=10)

        self.result_text = tk.StringVar()
        tk.Label(self.root, textvariable=self.result_text, justify="left", wraplength=400).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        last_city = self.settings.get_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)

    def display_weather(self):
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        weather_data = self.weather_service.get_weather_data(city_name)
        if weather_data:
            self.settings.set_last_city(city_name)
            self.update_display(weather_data)
        else:
            messagebox.showerror("Error", "Could not fetch weather data. Please try again.")

    def update_display(self, weather_data):
        self.result_text.set(
            f"Weather in {weather_data['city']}:\n"
            f"Temperature: {weather_data['temperature']}°C\n"
            f"Description: {weather_data['description']}\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Wind Speed: {weather_data['wind_speed']} m/s"
        )
        save_weather_to_csv(
    weather_data['city'],
    weather_data['temperature'],
    weather_data['description']
)
        messagebox.showinfo("Success", "Weather data saved successfully.")


def main():
    app = WeatherDashboard()
    app.root.mainloop()

if __name__ == "__main__":
    main()
