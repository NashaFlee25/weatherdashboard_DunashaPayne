"""Settings repository implementation."""

import json
import os
from typing import Optional
from src.domain.interfaces import ISettingsRepository


class SettingsRepository(ISettingsRepository):
    """File-based settings repository."""
    
    def __init__(self, settings_file: str = "config/user_settings.json"):
        self.settings_file = settings_file
        self._ensure_settings_file()
        self._settings = self._load_settings()
    
    def _ensure_settings_file(self) -> None:
        """Ensure settings file and directory exist."""
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        if not os.path.exists(self.settings_file):
            self._create_default_settings()
    
    def _create_default_settings(self) -> None:
        """Create default settings file."""
        default_settings = {
            "api_key": os.getenv("OPENWEATHER_API_KEY", ""),
            "temperature_units": "metric",
            "last_searched_city": None
        }
        with open(self.settings_file, 'w') as f:
            json.dump(default_settings, f, indent=4)
    
    def _load_settings(self) -> dict:
        """Load settings from file."""
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _save_settings(self) -> None:
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get_api_key(self) -> Optional[str]:
        """Get API key."""
        return self._settings.get("api_key") or os.getenv("OPENWEATHER_API_KEY")
    
    def get_default_units(self) -> str:
        """Get default temperature units."""
        return self._settings.get("temperature_units", "metric")
    
    def get_last_searched_city(self) -> Optional[str]:
        """Get last searched city."""
        return self._settings.get("last_searched_city")
    
    def save_last_searched_city(self, city: str) -> None:
        """Save last searched city."""
        self._settings["last_searched_city"] = city
        self._save_settings()
