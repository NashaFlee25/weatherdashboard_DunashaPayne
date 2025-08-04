"""
Handles OpenWeatherMap API requests and error handling.
"""
import requests
import os

class WeatherAPIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_weather(self, city):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"],
                "city": data["name"]
            }
        except requests.exceptions.HTTPError:
            return {"error": "Invalid city name or API error."}
        except requests.exceptions.RequestException:
            return {"error": "Connection error. Please try again."}

    def is_api_key_valid(self):
        # Simple check by querying a known city
        result = self.fetch_weather("London")
        return "error" not in result
