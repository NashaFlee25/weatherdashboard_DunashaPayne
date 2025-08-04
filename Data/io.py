"""
Data I/O module for weather dashboard
Handles reading and writing weather data
"""
import json
import csv
from typing import Dict, List, Any
from datetime import datetime


def save_weather_data(data: Dict[str, Any], filepath: str) -> bool:
    """Save weather data to a JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def load_weather_data(filepath: str) -> Dict[str, Any]:
    """Load weather data from a JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}


def export_to_csv(data: List[Dict[str, Any]], filepath: str) -> bool:
    """Export weather data to CSV format"""
    if not data:
        return False
    
    try:
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
