import csv
import os

def get_available_cities():
    """Get list of unique cities available in the weather CSV file."""
    filename = os.path.join(os.path.dirname(__file__), "..", "data", "team_weather.csv")
    cities = set()
    
    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Handle both old and new CSV formats
                city_name = row.get('city', row.get('City', '')).strip()
                if city_name:
                    cities.add(city_name)
    except FileNotFoundError:
        return []
    except Exception:
        return []
    
    return sorted(list(cities))

def get_city_options_for_dropdown():
    """Get list of cities formatted for dropdown options."""
    cities = get_available_cities()
    if not cities:
        return [{"value": "", "label": "No cities available"}]
    
    options = [{"value": "", "label": "Select a city..."}]
    for city in cities:
        options.append({"value": city, "label": city})
    
    return options

def compare_cities_from_csv(city1, city2):
    filename = os.path.join(os.path.dirname(__file__), "..", "data", "team_weather.csv")

    latest_data = {city1.lower(): None, city2.lower(): None}

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            
            for row in reversed(rows):
                # Handle both old and new CSV formats
                city_name = row.get('city', '').strip()
                if not city_name:
                    continue
                    
                city_key = city_name.lower()
                if city_key in latest_data and not latest_data[city_key]:
                    # Extract relevant data based on available columns
                    timestamp = row.get('timestamp', row.get('Timestamp', ''))
                    temperature = row.get('temperature', row.get('Temperature (F)', ''))
                    description = row.get('weather_description', row.get('Description', ''))
                    
                    latest_data[city_key] = (timestamp, city_name, temperature, description)
                    
                if all(latest_data.values()):
                    break
                    
    except FileNotFoundError:
        return "Weather history file not found."
    except Exception as e:
        return f"Error reading weather data: {e}"

    # Format the output
    city1_data = latest_data[city1.lower()]
    city2_data = latest_data[city2.lower()]

    if not city1_data or not city2_data:
        missing = [city for city, data in zip([city1, city2], [city1_data, city2_data]) if not data]
        return f"City/cities not found in weather history: {', '.join(missing)}"

    result = (
        f"📍 {city1_data[1]} (Last update: {city1_data[0]})\n"
        f"   🌡 Temp: {city1_data[2]}°F\n"
        f"   🌤 Condition: {city1_data[3]}\n\n"
        f"📍 {city2_data[1]} (Last update: {city2_data[0]})\n"
        f"   🌡 Temp: {city2_data[2]}°F\n"
        f"   🌤 Condition: {city2_data[3]}"
    )
    return result
