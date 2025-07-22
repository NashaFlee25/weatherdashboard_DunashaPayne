import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"

    def get_last_city(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    return settings.get('last_city', '')
        except:
            pass
        return ''

    def set_last_city(self, city):
        try:
            settings = {'last_city': city}
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except:
            pass
