import csv
import os
from typing import Dict
from collections import Counter

def calculate_stats_from_csv() -> Dict:
    """
    Calculate statistics from weather_log.csv file.
    
    Returns:
        Dictionary with min/max temperatures and weather description counts
    """
    if not os.path.isfile('weather_log.csv'):
        return {"min": None, "max": None, "counts": {}}
    
    temperatures = []
    descriptions = []
    
    try:
        with open('weather_log.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Extract numeric temperature value
                    temp_str = row['Temperature'].replace('°C', '').strip()
                    temperature = float(temp_str)
                    temperatures.append(temperature)
                    descriptions.append(row['Description'])
                except (ValueError, KeyError):
                    continue
    except FileNotFoundError:
        return {"min": None, "max": None, "counts": {}}
    
    if not temperatures:
        return {"min": None, "max": None, "counts": {}}
    
    min_temp = min(temperatures)
    max_temp = max(temperatures)
    description_counts = dict(Counter(descriptions))
    
    return {
        "min": min_temp,
        "max": max_temp,
        "counts": description_counts
    }
