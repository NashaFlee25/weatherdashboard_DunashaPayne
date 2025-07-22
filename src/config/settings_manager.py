import json
import os

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self._ensure_settings_file()

    def _ensure_settings_file(self):
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, "w") as f:
                json.dump({"last_city": ""}, f)

    def get_last_city(self):
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
                return settings.get("last_city", "")
        except:
            return ""

    def set_last_city(self, city):
        try:
            with open(self.settings_file, "r") as f:
                settings = json.load(f)
            settings["last_city"] = city
            with open(self.settings_file, "w") as f:
                json.dump(settings, f)
        except:
            pass
