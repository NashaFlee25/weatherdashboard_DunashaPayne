"""City comparison feature implementation."""

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime


class CityComparison:
    """Feature for comparing weather between two cities."""
    
    def __init__(self, weather_service):
        """Initialize city comparison feature."""
        self.weather_service = weather_service
        self.comparison_window = None
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
    
    def open_comparison_window(self):
        """Open the city comparison window."""
        if self.comparison_window and self.comparison_window.winfo_exists():
            self.comparison_window.lift()
            return
        
        self.comparison_window = tk.Toplevel()
        self.comparison_window.title("City Weather Comparison")
        self.comparison_window.geometry("700x500")
        
        self.setup_comparison_ui()
    
    def setup_comparison_ui(self):
        """Setup the comparison window UI."""
        main_frame = ttk.Frame(self.comparison_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Compare Cities Weather", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # City inputs
        ttk.Label(main_frame, text="City 1:").grid(row=1, column=0, sticky=tk.W)
        self.city1_var = tk.StringVar()
        city1_entry = ttk.Entry(main_frame, textvariable=self.city1_var, width=20)
        city1_entry.grid(row=1, column=1, padx=(5, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(main_frame, text="City 2:").grid(row=1, column=2, sticky=tk.W)
        self.city2_var = tk.StringVar()
        city2_entry = ttk.Entry(main_frame, textvariable=self.city2_var, width=20)
        city2_entry.grid(row=1, column=3, padx=(5, 0), sticky=(tk.W, tk.E))
        
        # Compare button
        compare_btn = ttk.Button(main_frame, text="Compare Weather", 
                                command=self.compare_cities)
        compare_btn.grid(row=2, column=0, columnspan=4, pady=(10, 20))
        
        # Results area
        self.results_text = tk.Text(main_frame, height=20, width=80)
        self.results_text.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, 
                                 command=self.results_text.yview)
        scrollbar.grid(row=3, column=4, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.comparison_window.columnconfigure(0, weight=1)
        self.comparison_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(3, weight=1)
    
    def compare_cities(self):
        """Compare weather between two cities."""
        city1 = self.city1_var.get().strip()
        city2 = self.city2_var.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Input Error", "Please enter both city names.")
            return
        
        if city1.lower() == city2.lower():
            messagebox.showwarning("Input Error", "Please enter different cities.")
            return
        
        try:
            # Get weather data for both cities
            weather1 = self.weather_service.get_current_weather(city1)
            weather2 = self.weather_service.get_current_weather(city2)
            
            if not weather1 or not weather2:
                messagebox.showerror("Error", "Could not retrieve weather data for one or both cities.")
                return
            
            # Display comparison
            self.display_comparison(weather1, weather2)
            
            # Log comparison
            self.log_comparison(weather1, weather2)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
    
    def display_comparison(self, weather1, weather2):
        """Display weather comparison in the text area."""
        self.results_text.delete(1.0, tk.END)
        
        comparison_text = f"""WEATHER COMPARISON
{'='*50}

{weather1['city']}, {weather1['country']} vs {weather2['city']}, {weather2['country']}

TEMPERATURE:
{weather1['city']}: {weather1['temperature']}°C (feels like {weather1['feels_like']}°C)
{weather2['city']}: {weather2['temperature']}°C (feels like {weather2['feels_like']}°C)
Difference: {abs(weather1['temperature'] - weather2['temperature']):.1f}°C

WEATHER CONDITION:
{weather1['city']}: {weather1['description'].title()}
{weather2['city']}: {weather2['description'].title()}

HUMIDITY:
{weather1['city']}: {weather1['humidity']}%
{weather2['city']}: {weather2['humidity']}%
Difference: {abs(weather1['humidity'] - weather2['humidity'])}%

WIND:
{weather1['city']}: {weather1['wind_speed']} m/s
{weather2['city']}: {weather2['wind_speed']} m/s
Difference: {abs(weather1['wind_speed'] - weather2['wind_speed']):.1f} m/s

PRESSURE:
{weather1['city']}: {weather1['pressure']} hPa
{weather2['city']}: {weather2['pressure']} hPa
Difference: {abs(weather1['pressure'] - weather2['pressure'])} hPa

VISIBILITY:
{weather1['city']}: {weather1['visibility']} km
{weather2['city']}: {weather2['visibility']} km

{'='*50}
Comparison completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        self.results_text.insert(tk.END, comparison_text)
    
    def log_comparison(self, weather1, weather2):
        """Log comparison data to CSV file."""
        try:
            log_file = os.path.join(self.data_dir, 'comparison_log.csv')
            
            # Create header if file doesn't exist
            if not os.path.exists(log_file):
                with open(log_file, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['timestamp', 'city1', 'temp1', 'desc1', 
                                   'city2', 'temp2', 'desc2', 'temp_diff'])
            
            # Append comparison data
            with open(log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                temp_diff = abs(weather1['temperature'] - weather2['temperature'])
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    weather1['city'], weather1['temperature'], weather1['description'],
                    weather2['city'], weather2['temperature'], weather2['description'],
                    round(temp_diff, 1)
                ])
                
        except Exception as e:
            print(f"Error logging comparison data: {e}")
