import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "weather_preferences.json"
        self.default_settings = {
            "last_city": "",
            "theme": "light"
        }
        self.current_settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Ensure all default keys exist
                    for key in self.default_settings:
                        if key not in loaded_settings:
                            loaded_settings[key] = self.default_settings[key]
                    return loaded_settings
            return self.default_settings.copy()
        except (json.JSONDecodeError, IOError):
            return self.default_settings.copy()

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.current_settings, f)

    def get_last_city(self):
        return self.current_settings.get("last_city", "")

    def set_last_city(self, city):
        self.current_settings["last_city"] = city
        self.save_settings()

    def get_theme(self):
        return self.current_settings.get("theme", "light")

    def set_theme(self, theme):
        self.current_settings["theme"] = theme
        self.save_settings()

    def clear_settings(self):
        """Clear all settings and return to defaults"""
        self.reset_to_defaults()
        if os.path.exists(self.settings_file):
            try:
                os.remove(self.settings_file)
            except OSError:
                pass

    def reset_to_defaults(self):
        """Reset settings to default values"""
        self.current_settings = self.default_settings.copy()
        self.save_settings()
