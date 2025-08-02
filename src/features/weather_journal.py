"""
Feature: Weather Journal logic.
"""
import pandas as pd
from datetime import datetime

class WeatherJournal:
    def __init__(self, filename="journal.csv"):
        self.filename = filename
        try:
            self.df = pd.read_csv(filename)
        except Exception:
            self.df = pd.DataFrame(columns=["date", "city", "temperature", "notes"])

    def add_entry(self, city, temperature, notes):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "city": city,
            "temperature": temperature,
            "notes": notes
        }
        self.df = pd.concat([self.df, pd.DataFrame([entry])], ignore_index=True)
        self.df.to_csv(self.filename, index=False)

    def get_entries(self):
        return self.df
