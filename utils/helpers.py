"""
Utility helper functions for the weather dashboard application.
"""
from typing import Optional


def get_weather_phrase(description: str) -> str:
    """
    Returns an emoji + phrase based on weather description keywords.
    
    Args:
        description: Weather description string
        
    Returns:
        String with emoji and encouraging phrase
    """
    if not description:
        return "🌈 Have a great day!"
    
    description_lower = description.lower()
    
    if "rain" in description_lower:
        return "🌧️ Grab an umbrella!"
    elif "clear" in description_lower:
        return "☀️ Enjoy the sunshine!"
    elif "cloud" in description_lower:
        return "☁️ Cozy day ahead!"
    else:
        return "🌈 Have a great day!"


def suggest_activity(temperature: float, description: str) -> str:
    """
    Suggest an activity based on weather conditions.
    
    Args:
        temperature: Temperature in Celsius
        description: Weather description
        
    Returns:
        Activity suggestion string
    """
    description_lower = description.lower()
    
    if temperature > 25 and "clear" in description_lower:
        return "🏖️ Perfect day for the beach!"
    elif temperature < 5:
        return "🏠 Great day to stay cozy indoors!"
    elif "rain" in description_lower:
        return "📚 Good time to read a book!"
    elif 15 <= temperature <= 25:
        return "🚶 Nice weather for a walk!"
    else:
        return "🌟 Enjoy your day!"
