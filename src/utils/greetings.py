from datetime import datetime


def get_personalized_greeting(name: str) -> str:
    """
    Generate a personalized greeting based on the current time of day.
    
    Args:
        name: The name to include in the greeting
        
    Returns:
        A personalized greeting string with appropriate emoji
    """
    current_hour = datetime.now().hour
    
    if current_hour < 12:
        return f"Good morning, {name}! 🌅"
    elif current_hour < 18:
        return f"Good afternoon, {name}! ☀️"
    else:
        return f"Good evening, {name}! 🌙"
