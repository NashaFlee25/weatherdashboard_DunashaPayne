"""
Settings Manager

Handles application settings persistence using JSON configuration file.
Supports theme preferences, last searched city, and other user preferences.
"""
import json
import os
from typing import Optional, Dict, Any


class SettingsManager:
    """Manages application settings with JSON file persistence."""
    
    def __init__(self):
        """Initialize settings manager and load configuration."""
        self._config_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        self._config_path = os.path.join(self._config_dir, 'settings.json')
        self._config: Dict[str, Any] = {}
        
        # Ensure config directory exists
        os.makedirs(self._config_dir, exist_ok=True)
        
        # Load existing configuration or create default
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from JSON file or create default config."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            else:
                # Create default configuration
                self._config = {
                    'theme': 'light',
                    'last_city': '',
                    'window_geometry': '800x600',
                    'auto_load_last_city': True
                }
                self._save_config()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load settings file. Using defaults. Error: {e}")
            self._config = {
                'theme': 'light',
                'last_city': '',
                'window_geometry': '800x600',
                'auto_load_last_city': True
            }
    
    def _save_config(self) -> None:
        """Save current configuration to JSON file."""
        try:
            with open(self._config_path, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save settings file. Error: {e}")
    
    def get_theme(self) -> str:
        """Return the saved theme, defaulting to 'light' if unset."""
        return self._config.get('theme', 'light')
    
    def save_theme(self, theme: str) -> None:
        """Save the selected theme and write back to settings.json."""
        if theme in ['light', 'dark']:
            self._config['theme'] = theme
            self._save_config()
        else:
            raise ValueError(f"Invalid theme '{theme}'. Must be 'light' or 'dark'.")
    
    def get_last_city(self) -> Optional[str]:
        """Return the last searched city, or None if not set."""
        last_city = self._config.get('last_city', '')
        return last_city if last_city else None
    
    def save_last_city(self, city: str) -> None:
        """Save the last searched city."""
        self._config['last_city'] = city.strip()
        self._save_config()
    
    def get_window_geometry(self) -> str:
        """Return the saved window geometry."""
        return self._config.get('window_geometry', '800x600')
    
    def save_window_geometry(self, geometry: str) -> None:
        """Save the window geometry."""
        self._config['window_geometry'] = geometry
        self._save_config()
    
    def get_auto_load_last_city(self) -> bool:
        """Return whether to automatically load the last searched city."""
        return self._config.get('auto_load_last_city', True)
    
    def save_auto_load_last_city(self, auto_load: bool) -> None:
        """Save the auto-load last city preference."""
        self._config['auto_load_last_city'] = auto_load
        self._save_config()
    
    def get_all_settings(self) -> Dict[str, Any]:
        """Return a copy of all current settings."""
        return self._config.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self._config = {
            'theme': 'light',
            'last_city': '',
            'window_geometry': '800x600',
            'auto_load_last_city': True
        }
        self._save_config()
