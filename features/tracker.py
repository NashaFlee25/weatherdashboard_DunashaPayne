import csv
import os

def save_weather_to_csv(city, temperature, description):
    """
    Save weather data to a CSV file.
    """
    file_exists = os.path.isfile('weather_log.csv')
    with open('weather_log.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['City', 'Temperature', 'Description'])
        writer.writerow([city, temperature, description])
