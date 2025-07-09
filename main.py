import requests  
from dotenv import load_dotenv 
import os
import tkinter as tk
from tkinter import messagebox

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

# Function to display weather data in the GUI
def display_weather():
    city_name = city_entry.get()
    if not city_name:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        messagebox.showerror("Error", "API key not found. Please set it in the .env file.")
        return

    weather_data = fetch_weather(city_name, api_key)
    if weather_data:
        result_text.set(
            f"Weather in {city_name}: {weather_data['weather'][0]['description'].capitalize()}\n"
            f"Temperature: {weather_data['main']['temp']}°C\n"
            f"Humidity: {weather_data['main']['humidity']}%\n"
            f"Wind Speed: {weather_data['wind']['speed']} m/s\n"
            f"Visibility: {weather_data['visibility'] / 1000} km\n"
            f"Cloudiness: {weather_data['clouds']['all']}%\n"
            f"Sunrise: {weather_data['sys']['sunrise']} (Unix timestamp)\n"
            f"Sunset: {weather_data['sys']['sunset']} (Unix timestamp)\n"
            f"Fog: {weather_data.get('fog', 'No fog data available')}\n"
            f"Rain: {weather_data.get('rain', 'No rain data available')}"
        )
    else:
        result_text.set("Failed to retrieve weather data. Please try again.")

# Main app logic
def main():
    global city_entry, result_text

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Weather Dashboard")
    root.geometry("500x300")

    # Create and place widgets
    tk.Label(root, text="Enter City Name:").grid(row=0, column=0, padx=10, pady=10)
    city_entry = tk.Entry(root, width=30)
    city_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(root, text="Get Weather", command=display_weather).grid(row=1, column=0, columnspan=2, pady=10)

    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, justify="left", wraplength=400).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
