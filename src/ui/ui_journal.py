"""
Weather Journal page: add/view journal entries.
"""
import customtkinter as ctk
from src.features.weather_journal import WeatherJournal

class JournalPage(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.journal = WeatherJournal()
        self.city_entry = ctk.CTkEntry(self, placeholder_text="City")
        self.city_entry.pack(pady=5)
        self.temp_entry = ctk.CTkEntry(self, placeholder_text="Temperature")
        self.temp_entry.pack(pady=5)
        self.notes_entry = ctk.CTkEntry(self, placeholder_text="Notes")
        self.notes_entry.pack(pady=5)
        self.add_btn = ctk.CTkButton(self, text="Add Entry", command=self.add_entry)
        self.add_btn.pack(pady=5)
        self.entries_label = ctk.CTkLabel(self, text="Journal Entries:")
        self.entries_label.pack(pady=5)
        self.entries_box = ctk.CTkTextbox(self)
        self.entries_box.pack(pady=5, fill="both", expand=True)
        self.refresh_entries()

    def add_entry(self):
        city = self.city_entry.get()
        temp = self.temp_entry.get()
        notes = self.notes_entry.get()
        self.journal.add_entry(city, temp, notes)
        self.refresh_entries()

    def refresh_entries(self):
        entries = self.journal.get_entries()
        self.entries_box.delete("1.0", "end")
        for _, row in entries.iterrows():
            self.entries_box.insert("end", f"{row['date']} | {row['city']} | {row['temperature']}°C | {row['notes']}\n")
