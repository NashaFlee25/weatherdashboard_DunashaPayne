from pathlib import Path
from datetime import datetime
import csv
from typing import Dict


def compare_cities(city1: str, city2: str, n: int = 1) -> Dict[str, Dict]:
    """
    Load `data/team_weather_data.csv`, find the last `n` entries
    for each city, and return their latest weather dicts under keys city1 & city2.
    """
    # Look for team_weather_data.csv in the data directory
    path = Path(__file__).parent.parent / "data" / "team_weather_data.csv"
    rows = []
    
    try:
        with path.open(newline="") as f:
            reader = csv.DictReader(f)
            for r in reader:
                if r["city"].lower() in (city1.lower(), city2.lower()):
                    rows.append({
                        **r,
                        "temperature": float(r["temperature"]),
                        "humidity": int(r["humidity"]),
                        "pressure": int(r["pressure"]),
                        "timestamp": datetime.fromisoformat(r["timestamp"])
                    })
    except FileNotFoundError:
        # Fallback to weather_history.csv if team_weather_data.csv doesn't exist
        fallback_path = Path(__file__).parent.parent / "weather_history.csv"
        try:
            with fallback_path.open(newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if r["city"].lower() in (city1.lower(), city2.lower()):
                        rows.append({
                            **r,
                            "temperature": float(r["temperature"]),
                            "humidity": int(r["humidity"]),
                            "pressure": int(r["pressure"]),
                            "timestamp": datetime.fromisoformat(r["timestamp"])
                        })
        except FileNotFoundError:
            return {city1: {}, city2: {}}
    
    def latest_for(city):
        filt = [r for r in rows if r["city"].lower() == city.lower()]
        return filt[-1] if filt else {}
    
    return {city1: latest_for(city1), city2: latest_for(city2)}
