"""
Weather tracking functionality including data persistence and helper functions.
"""
import csv
import os
from datetime import datetime
from collections import Counter


def save_weather_to_csv(weather_data, filename="weather_history.csv"):
    """Save weather data to CSV file"""
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'city', 'country', 'temperature', 'feels_like', 
                     'description', 'humidity', 'pressure']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'city': weather_data['city'],
            'country': weather_data['country'],
            'temperature': weather_data['temperature'],
            'feels_like': weather_data['feels_like'],
            'description': weather_data['description'],
            'humidity': weather_data['humidity'],
            'pressure': weather_data['pressure']
        })


def read_last_n_entries(n=10, filename="weather_history.csv"):
    """Read the last n entries from the CSV file"""
    if not os.path.exists(filename):
        return []
    
    entries = []
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        entries = list(reader)
    
    # Return last n entries (most recent first)
    return entries[-n:][::-1] if entries else []


def calculate_stats_from_csv(filename="weather_history.csv"):
    """Calculate statistics from weather data in CSV file"""
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    
    if not data:
        return None
    
    temperatures = [float(row['temperature']) for row in data]
    humidities = [float(row['humidity']) for row in data]
    pressures = [float(row['pressure']) for row in data]
    cities = [f"{row['city']}, {row['country']}" for row in data]
    
    # Calculate statistics
    stats = {
        'total_searches': len(data),
        'avg_temp': sum(temperatures) / len(temperatures),
        'max_temp': max(temperatures),
        'min_temp': min(temperatures),
        'avg_humidity': sum(humidities) / len(humidities),
        'avg_pressure': sum(pressures) / len(pressures),
        'top_cities': Counter(cities).most_common()
    }
    
    return stats


def get_weather_phrase(temperature, description):
    """Generate a descriptive phrase based on weather conditions"""
    description = description.lower()
    
    # Temperature-based phrases
    if temperature < 0:
        temp_phrase = "Bundle up, it's freezing!"
    elif temperature < 10:
        temp_phrase = "It's quite cold out there."
    elif temperature < 20:
        temp_phrase = "Perfect weather for a light jacket."
    elif temperature < 30:
        temp_phrase = "Great weather to be outside!"
    else:
        temp_phrase = "It's getting quite hot!"
    
    # Weather condition phrases
    if "rain" in description:
        condition_phrase = "Don't forget your umbrella!"
    elif "snow" in description:
        condition_phrase = "Winter wonderland awaits!"
    elif "clear" in description or "sun" in description:
        condition_phrase = "Perfect day for outdoor activities!"
    elif "cloud" in description:
        condition_phrase = "Cloudy but pleasant."
    elif "storm" in description or "thunder" in description:
        condition_phrase = "Stay safe indoors!"
    else:
        condition_phrase = "Check the sky before heading out."
    
    return f"{temp_phrase} {condition_phrase}"
