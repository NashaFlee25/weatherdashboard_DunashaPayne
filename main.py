"""
Weather Dashboard Application - Main Entry Point

Clean architecture implementation with proper separation of concerns.
"""

import sys
import os
import logging
from typing import Optional

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.config.settings import WeatherConfig, UIConfig, AppConfig
from src.infrastructure.repositories.weather_repository import WeatherRepository
from src.infrastructure.repositories.settings_repository import SettingsRepository
from src.application.services.weather_service import WeatherService
from src.presentation.controllers.weather_controller import WeatherController
from src.presentation.main_window import MainWindow


def setup_logging(log_level: str = "INFO"):
    """Setup application logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('weather_dashboard.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_app_config() -> Optional[AppConfig]:
    """Create application configuration."""
    try:
        settings_repo = SettingsRepository()
        api_key = settings_repo.get_api_key()
        
        if not api_key:
            print("Error: OpenWeather API key not found.")
            print("Please set OPENWEATHER_API_KEY environment variable or configure in settings.")
            return None
        
        weather_config = WeatherConfig(
            api_key=api_key,
            temperature_units=settings_repo.get_default_units()
        )
        
        ui_config = UIConfig()
        
        return AppConfig(
            weather=weather_config,
            ui=ui_config
        )
    except Exception as e:
        print(f"Error creating app configuration: {e}")
        return None


def create_dependencies(config: AppConfig):
    """Create and wire up dependencies."""
    # Repositories
    settings_repo = SettingsRepository()
    weather_repo = WeatherRepository(config.weather)
    
    # Services
    weather_service = WeatherService(weather_repo, settings_repo)
    
    # Controllers
    weather_controller = WeatherController(weather_service)
    
    # Main Window
    main_window = MainWindow(weather_controller, settings_repo, config.ui)
    
    return main_window


def main():
    """Main entry point for the Weather Dashboard application."""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Weather Dashboard Application")
        
        # Create configuration
        config = create_app_config()
        if not config:
            sys.exit(1)
        
        # Create dependencies
        main_window = create_dependencies(config)
        
        # Create and run the application
        root = main_window.create_window()
        logger.info("Application window created successfully")
        
        main_window.run()
        
    except Exception as e:
        logging.error(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
