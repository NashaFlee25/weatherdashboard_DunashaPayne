"""
API key loader using environment variables.
"""
import os
from dotenv import load_dotenv

def load_api_key():
    """Load API key from environment variables."""
    load_dotenv()
    api_key = os.getenv('API_KEY') or os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Please set API_KEY or OPENWEATHER_API_KEY in .env file")
    return api_key