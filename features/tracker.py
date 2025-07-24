import csv
from datetime import datetime

def save_weather_to_csv(city, temperature, condition):
    filename = "weather_history_Dunasha.csv"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, city, temperature, condition])

save_weather_to_csv(city_name, temp, weather_description)
