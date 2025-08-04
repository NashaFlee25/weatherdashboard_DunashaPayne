"""
Application constants and configuration values.
"""

# Application window settings
WINDOW_TITLE: str = "Weather Dashboard"
WINDOW_SIZE: str = "800x600"
MIN_WINDOW_SIZE: tuple = (600, 400)

# Modern theme settings (using CustomTkinter themes)
DEFAULT_THEME: str = "dark"
AVAILABLE_THEMES: list = ["light", "dark", "system"]

# Weather data settings
DEFAULT_HISTORY_ENTRIES: int = 10
CSV_FILENAME: str = "weather_data.csv"
JOURNAL_FILENAME: str = "journal.csv"

# API settings
API_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
API_TIMEOUT: int = 10
