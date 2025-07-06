import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to fetch weather data from OpenWeather API
def fetch_weather(city_name, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 401:
        print("Error: Invalid API key. Please check your API key in the .env file.")
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch weather data (Status Code: {response.status_code})")
        return None

# Main app logic
def main():
    print("Welcome to the Weather Dashboard!")
    api_key = os.getenv("OPENWEATHER_API_KEY")  # Get API key from .env file
    if not api_key:
        print("Error: API key not found. Please set it in the .env file.")
        return
    city_name = input("Enter the name of the city: ")
    weather_data = fetch_weather(city_name, api_key)
    if weather_data:
        print(f"Weather in {city_name}: {weather_data['weather'][0]['description'].capitalize()}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")

if __name__ == "__main__":
    main()
