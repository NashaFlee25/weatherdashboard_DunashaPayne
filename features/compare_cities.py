import csv
import os

def compare_cities_from_csv(city1, city2):
    filename = os.path.join(os.path.dirname(__file__), "..", "data", "team_weather.csv")

    latest_data = {city1.lower(): None, city2.lower(): None}

    try:
        with open(filename, mode='r') as file:
            reader = list(csv.reader(file))
            for row in reversed(reader):
                if len(row) < 4:
                    continue  # Skip bad rows
                date, city, temp, condition = row
                city_key = city.lower()
                if city_key in latest_data and not latest_data[city_key]:
                    latest_data[city_key] = (date, city, temp, condition)
                if all(latest_data.values()):
                    break
    except FileNotFoundError:
        return "Weather history file not found."

    # Format the output
    city1_data = latest_data[city1.lower()]
    city2_data = latest_data[city2.lower()]

    if not city1_data or not city2_data:
        return "One or both cities were not found in the weather history."

    result = (
        f"📍 {city1_data[1]} (Last update: {city1_data[0]})\n"
        f"   🌡 Temp: {city1_data[2]}°C\n"
        f"   🌤 Condition: {city1_data[3]}\n\n"
        f"📍 {city2_data[1]} (Last update: {city2_data[0]})\n"
        f"   🌡 Temp: {city2_data[2]}°C\n"
        f"   🌤 Condition: {city2_data[3]}"
    )
    return result
