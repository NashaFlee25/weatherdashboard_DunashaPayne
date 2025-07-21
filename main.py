import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os
import tkinter as tk
from tkinter import messagebox
import json
from typing import Optional, Dict, Any

# Load environment variables from .env file
load_dotenv()

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def fetch_weather(self, city_name: str) -> Optional[Dict[str, Any]]:
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                print("Error: Invalid API key. Please check your API key in the .env file.")
            elif response.status_code == 404:
                messagebox.showerror("Error", f"City '{city_name}' not found. Please check the spelling and try again.")
            else:
                print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        return None

class UserSettings:
    def __init__(self, filename: str = "user_settings.json"):
        self.filename = filename

    def save(self, settings: Dict[str, Any]) -> None:
        try:
            with open(self.filename, "w") as file:
                json.dump(settings, file, indent=4)
            print(f"Settings saved to {self.filename}")
        except IOError as e:
            print(f"Error saving settings: {e}")

    def load(self) -> Optional[Dict[str, Any]]:
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    return json.load(file)
        except IOError as e:
            print(f"Error loading settings: {e}")
        return None

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set it in the .env file.")
        self.weather_api = WeatherAPI(self.api_key)
        self.user_settings = UserSettings()
        self.root = tk.Tk()
        self.result_text = tk.StringVar()

    def display_weather(self) -> None:
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        weather_data = self.weather_api.fetch_weather(city_name)
        if not weather_data:
            messagebox.showerror("Error", "City not found. Please try again.")
            return

        self.user_settings.save({"last_searched_city": city_name})
        self.result_text.set(self.format_weather_data(city_name, weather_data))

    def format_weather_data(self, city_name: str, weather_data: Dict[str, Any]) -> str:
        try:
            return (
                f"Weather in {city_name}: {weather_data['weather'][0]['description'].capitalize()}\n"
                f"Temperature: {weather_data['main']['temp']}°C\n"
                f"Humidity: {weather_data['main']['humidity']}%\n"
                f"Wind Speed: {weather_data['wind']['speed']} m/s\n"
                f"Visibility: {weather_data['visibility'] / 1000} km\n"
                f"Cloudiness: {weather_data['clouds']['all']}%\n"
                f"Sunrise: {self.format_unix_timestamp(weather_data['sys']['sunrise'])}\n"
                f"Sunset: {self.format_unix_timestamp(weather_data['sys']['sunset'])}\n"
                f"Fog: {weather_data.get('fog', 'No fog data available')}\n"
                f"Rain: {weather_data.get('rain', 'No rain data available')}"
            )
        # Handle missing keys gracefully
        except KeyError as e:
            print(f"Error formatting weather data: Missing key {e}")
            return "Error formatting weather data."

    @staticmethod
    def format_unix_timestamp(timestamp: int) -> str:
        from datetime import datetime
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def run(self) -> None:
        self.root.title("Weather Dashboard")
        self.root.geometry("500x300")

        tk.Label(self.root, text="Enter City Name:").grid(row=0, column=0, padx=10, pady=10)
        self.city_entry = tk.Entry(self.root, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Get Weather", command=self.display_weather).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(self.root, textvariable=self.result_text, justify="left", wraplength=400).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        last_settings = self.user_settings.load()
        if last_settings and "last_searched_city" in last_settings:
            self.city_entry.insert(0, last_settings["last_searched_city"])

        self.root.mainloop()

def main() -> None:
    try:
        dashboard = WeatherDashboard()
        dashboard.run()
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
