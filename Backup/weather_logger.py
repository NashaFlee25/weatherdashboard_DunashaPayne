import csv
import os
from datetime import datetime

def log_weather_data(city, temp, description):
    """
    Log weather data to a CSV file.
    Creates the file with headers if it doesn't exist, otherwise appends data.
    """
    file_path = 'weather_log.csv'
    file_exists = os.path.exists(file_path)
    
    with open(file_path, 'a', newline='') as csvfile:
        fieldnames = ['city', 'date', 'temperature', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'city': city,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': temp,
            'description': description
        })
