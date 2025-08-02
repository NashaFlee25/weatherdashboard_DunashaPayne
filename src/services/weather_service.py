class WeatherService:
    """
    Service to fetch weather data for a given city.
    Replace the get_weather_data method with actual API integration as needed.
    """
    def get_weather_data(self, city_name):
        # Dummy data for demonstration; replace with real API call
        return {
            'city': city_name,
            'temperature': 22,
            'description': 'Clear sky',
            'humidity': 55,
            'wind_speed': 3.5
        }
