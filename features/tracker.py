import csv
from datetime import datetime
import os

def save_weather_to_csv(city, temperature, condition):
    filename = os.path.join(os.path.dirname(__file__), "..", "data", "weather_history_Dunasha.csv")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, city, temperature, condition])

# Optional test block
if __name__ == "__main__":
    city = "New York"
    temperature = 27.3
    condition = "Cloudy"
    save_weather_to_csv(city, temperature, condition)
