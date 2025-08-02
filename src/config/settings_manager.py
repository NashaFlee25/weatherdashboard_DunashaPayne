import os
import json

class SettingsManager:
    """
    Manages application settings, such as the last searched city.
    """
    SETTINGS_FILE = 'settings.json'

    def __init__(self):
        self.settings = self._load_settings()

    def _load_settings(self):
        if os.path.exists(self.SETTINGS_FILE):
            with open(self.SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {}

    def get_last_city(self):
        return self.settings.get('last_city', '')

    def set_last_city(self, city):
        self.settings['last_city'] = city
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f)
