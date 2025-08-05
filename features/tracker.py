"""
Weather tracking functionality including data persistence and helper functions.
"""
import csv
import os
from datetime import datetime
from collections import Counter
from typing import List, Dict
from pathlib import Path


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


def get_personalized_greeting(name):
    """
    Generate a personalized greeting with time-of-day emoji.
    
    Args:
        name: User's name
        
    Returns:
        String with personalized greeting and appropriate emoji
    """
    current_hour = datetime.now().hour
    
    if 5 <= current_hour < 12:
        return f"Good morning, {name}! 🌅"
    elif 12 <= current_hour < 18:
        return f"Good afternoon, {name}! ☀️"
    else:
        return f"Good evening, {name}! 🌙"


def get_weather_phrase(temperature, description):
    """
    Generate a weather phrase with emoji based on temperature and description.
    
    Args:
        temperature: Temperature in Celsius
        description: Weather description from API
        
    Returns:
        String with emoji and descriptive phrase
    """
    description_lower = description.lower()
    
    if "rain" in description_lower or "drizzle" in description_lower or "shower" in description_lower:
        return "🌧️ Don't forget your umbrella!"
    elif "clear" in description_lower or "sun" in description_lower:
        return "☀️ Perfect sunshine day!"
    elif "cloud" in description_lower or "overcast" in description_lower:
        return "☁️ Cozy clouds above!"
    else:
        return "🌈 Enjoy your day!"


def load_history() -> List[Dict]:
    """
    Load weather history from CSV file.
    
    Returns:
        List of dictionaries containing history data with keys:
        'timestamp', 'city', 'temp', 'condition'
    """
    history_data = []
    
    try:
        # Use the same filename as save_weather_to_csv function
        csv_path = "weather_history.csv"
        
        if not os.path.exists(csv_path):
            return history_data
        
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract data with fallback for missing fields
                timestamp = row.get("timestamp", "").strip()
                city = row.get("city", "").strip()
                country = row.get("country", "").strip()
                temperature = row.get("temperature", "").strip()
                description = row.get("description", "").strip()
                
                # Format city display
                if city and country:
                    city_display = f"{city}, {country}"
                else:
                    city_display = city or "Unknown"
                
                # Format temperature display
                if temperature:
                    try:
                        temp_value = float(temperature)
                        temp_display = f"{temp_value:.1f}°C"
                    except ValueError:
                        temp_display = temperature
                else:
                    temp_display = "N/A"
                
                # Format condition display
                condition_display = description.title() if description else "N/A"
                
                # Only add entries with at least timestamp and city
                if timestamp and city:
                    history_data.append({
                        "timestamp": timestamp,
                        "city": city_display,
                        "temp": temp_display,
                        "condition": condition_display
                    })
    
    except Exception as e:
        print(f"Error loading history from CSV: {e}")
    
    return history_data
