from pathlib import Path
from datetime import datetime
import csv
from typing import Dict


def compare_cities(city1: str, city2: str, n: int = 1) -> Dict[str, Dict]:
    """
    Load `team_weather_data.csv`, find the last `n` entries
    for each city, and return their latest weather dicts under keys city1 & city2.
    """
    path = Path(__file__).parent.parent / "data" / "team_weather_data.csv"
    rows = []
    
    try:
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                # Skip rows with empty city names
                city_name = r.get("city", "").strip()
                if not city_name:
                    continue
                    
                # Check if this row matches either city (case-insensitive)
                if city_name.lower() not in (city1.lower(), city2.lower()):
                    continue
                
                # Try to get temperature from multiple possible columns
                temp_str = ""
                temp_cols = ["temperature", "temp", "temp_f"]
                for temp_col in temp_cols:
                    val = r.get(temp_col, "").strip()
                    if val and val != "0" and val != "0.0":
                        temp_str = val
                        break
                
                # Try to get humidity from multiple possible columns  
                hum_str = ""
                hum_cols = ["humidity", "humidity_pct"]
                for hum_col in hum_cols:
                    val = r.get(hum_col, "").strip()
                    if val and val != "0" and val != "0.0":
                        hum_str = val
                        break
                
                # Try to get pressure - use default if not available
                pres_str = ""
                pres_cols = ["pressure"]
                for pres_col in pres_cols:
                    val = r.get(pres_col, "").strip()
                    if val and val != "0" and val != "0.0":
                        pres_str = val
                        break
                
                # If we don't have temperature and humidity (minimum required), skip
                if not temp_str or not hum_str:
                    continue
                
                try:
                    # Convert temperature 
                    temp = float(temp_str)
                    # Convert Fahrenheit to Celsius if needed (assuming > 50 means Fahrenheit)
                    if temp > 50:
                        temp = (temp - 32) * 5/9
                    
                    hum = int(float(hum_str))
                    
                    # Use default pressure if not available
                    if pres_str:
                        pres = int(float(pres_str))
                    else:
                        pres = 1013  # Default atmospheric pressure
                        
                except (ValueError, TypeError):
                    continue   # skip any row where conversion fails
                
                # Handle timestamp
                timestamp_str = r.get("timestamp", "").strip()
                if not timestamp_str:
                    # Try alternative timestamp columns
                    for ts_col in ["datetime", "dt"]:
                        if ts_col in r and r[ts_col].strip():
                            timestamp_str = r[ts_col].strip()
                            break
                
                # Parse timestamp with multiple format attempts
                timestamp = None
                if timestamp_str:
                    timestamp_formats = [
                        "%Y-%m-%dT%H:%M:%S.%f",  # ISO format with microseconds
                        "%Y-%m-%dT%H:%M:%S",     # ISO format
                        "%Y-%m-%d %H:%M:%S",     # Space separated
                        "%Y-%m-%d %H:%M",        # Without seconds
                        "%Y-%m-%d"               # Date only
                    ]
                    
                    for fmt in timestamp_formats:
                        try:
                            timestamp = datetime.strptime(timestamp_str, fmt)
                            break
                        except ValueError:
                            continue
                
                if not timestamp:
                    timestamp = datetime.now()  # Use current time if parsing fails
                
                # Get weather description from various possible columns
                weather_desc = ""
                desc_cols = ["weather_description", "description", "weather_main"]
                for desc_col in desc_cols:
                    val = r.get(desc_col, "").strip()
                    if val:
                        weather_desc = val
                        break
                
                if not weather_desc:
                    weather_desc = "Unknown"
                
                rows.append({
                    "city": city_name,
                    "temperature": temp,
                    "humidity": hum,
                    "pressure": pres,
                    "weather_description": weather_desc,
                    "timestamp": timestamp
                })
                
    except FileNotFoundError:
        return {city1: {}, city2: {}}
    except Exception as e:
        return {city1: {}, city2: {}}
    
    def latest_for(city):
        # Find all rows for this city (case-insensitive)
        filt = [r for r in rows if r["city"].lower() == city.lower()]
        if not filt:
            return {}
        # Sort by timestamp and return the latest
        filt.sort(key=lambda x: x["timestamp"])
        return filt[-1]
    
    return {city1: latest_for(city1), city2: latest_for(city2)}
