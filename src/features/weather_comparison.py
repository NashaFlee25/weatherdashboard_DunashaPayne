import tkinter as tk
from tkinter import ttk
import pandas as pd
import os

class WeatherComparison:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.csv_file_path = "team_weather.csv"
        self.city_names = []
        self.selected_city1 = tk.StringVar()
        self.selected_city2 = tk.StringVar()
        
        # Load city names from CSV
        self.load_cities_from_csv()
        
        # Create UI elements
        self.create_comparison_ui()
        
    def load_cities_from_csv(self):
        """Read CSV file and extract unique city names."""
        try:
            if os.path.exists(self.csv_file_path):
                df = pd.read_csv(self.csv_file_path)
                # Assuming city names are in a column named 'City' or similar
                # Adjust column name based on your CSV structure
                if 'City' in df.columns:
                    self.city_names = sorted(df['City'].dropna().unique().tolist())
                elif 'city' in df.columns:
                    self.city_names = sorted(df['city'].dropna().unique().tolist())
                else:
                    # If column name is different, use the first column
                    self.city_names = sorted(df.iloc[:, 0].dropna().unique().tolist())
            else:
                print(f"CSV file {self.csv_file_path} not found.")
                self.city_names = []
        except Exception as e:
            print(f"Error loading cities from CSV: {e}")
            self.city_names = []
    
    def create_comparison_ui(self):
        """Create the comparison UI with two dropdown menus."""
        # Main frame for comparison
        comparison_frame = ttk.LabelFrame(self.parent_frame, text="City Comparison", padding="10")
        comparison_frame.pack(fill="x", padx=10, pady=5)
        
        # City 1 selection
        city1_frame = ttk.Frame(comparison_frame)
        city1_frame.pack(side="left", padx=(0, 20))
        
        ttk.Label(city1_frame, text="City 1:").pack(anchor="w")
        self.city1_dropdown = ttk.Combobox(
            city1_frame,
            textvariable=self.selected_city1,
            values=self.city_names,
            state="readonly",
            width=20
        )
        self.city1_dropdown.pack(pady=5)
        self.city1_dropdown.bind('<<ComboboxSelected>>', self.on_city1_selected)
        
        # City 2 selection
        city2_frame = ttk.Frame(comparison_frame)
        city2_frame.pack(side="left")
        
        ttk.Label(city2_frame, text="City 2:").pack(anchor="w")
        self.city2_dropdown = ttk.Combobox(
            city2_frame,
            textvariable=self.selected_city2,
            values=self.city_names,
            state="readonly",
            width=20
        )
        self.city2_dropdown.pack(pady=5)
        self.city2_dropdown.bind('<<ComboboxSelected>>', self.on_city2_selected)
        
        # Refresh button to reload cities from CSV
        refresh_btn = ttk.Button(
            comparison_frame,
            text="Refresh Cities",
            command=self.refresh_cities
        )
        refresh_btn.pack(side="right", padx=(20, 0))
    
    def on_city1_selected(self, event):
        """Handle City 1 dropdown selection."""
        selected_city = self.selected_city1.get()
        print(f"City 1 selected: {selected_city}")
        # Store the selected value - you can add more logic here
        
    def on_city2_selected(self, event):
        """Handle City 2 dropdown selection."""
        selected_city = self.selected_city2.get()
        print(f"City 2 selected: {selected_city}")
        # Store the selected value - you can add more logic here
    
    def refresh_cities(self):
        """Refresh the city list from CSV and update dropdowns."""
        self.load_cities_from_csv()
        self.city1_dropdown['values'] = self.city_names
        self.city2_dropdown['values'] = self.city_names
        print("City list refreshed from CSV")
    
    def get_selected_cities(self):
        """Return the currently selected cities."""
        return {
            'city1': self.selected_city1.get(),
            'city2': self.selected_city2.get()
        }
    
    def set_selected_cities(self, city1=None, city2=None):
        """Programmatically set selected cities."""
        if city1 and city1 in self.city_names:
            self.selected_city1.set(city1)
        if city2 and city2 in self.city_names:
            self.selected_city2.set(city2)
