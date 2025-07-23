from dotenv import load_dotenv
import os


class Config:
    API_KEY = os.getenv("API_KEY")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    @classmethod
    def initialize(cls):
        # Load environment variables from .env file
        load_dotenv()
        
        # Access the API key
        cls.API_KEY = os.getenv("API_KEY")
        if not cls.API_KEY:
            raise ValueError("API_KEY not found in environment variables.")

# Initialize configuration when module is imported
Config.initialize()
