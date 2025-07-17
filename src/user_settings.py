import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

class UserSettings:
    def __init__(self, settings_file: str = "data/settings.json"):
        self.settings_file = settings_file
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict:
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"api_key": "", "default_city": "", "theme": "light"}

    def save_settings(self):
        Path(self.settings_file).parent.mkdir(exist_ok=True)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

class WeatherHistory:
    def __init__(self, history_file: str = "data/weather_history.json"):
        self.history_file = history_file
        self.history = self._load_history()

    def add_entry(self, city: str, weather_data: Dict[str, Any]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "city": city,
            "data": weather_data
        }
        self.history.append(entry)
        self._save_history()

    def _load_history(self) -> List:
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_history(self):
        Path(self.history_file).parent.mkdir(exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f)
