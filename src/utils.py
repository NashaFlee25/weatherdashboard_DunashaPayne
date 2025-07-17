from datetime import datetime

def format_timestamp(timestamp: str) -> str:
    """Convert ISO timestamp to readable format"""
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit"""
    return (kelvin - 273.15) * 9/5 + 32
