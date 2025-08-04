"""
GUI package for the Weather Dashboard application.
"""
from .dashboard import WeatherDashboard


def run_app() -> None:
    """
    Launch the Weather Dashboard application.
    """
    app = WeatherDashboard()
    app.run()
