import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv
from src.services.weather_service import WeatherService
from src.config.settings_manager import SettingsManager
from features.tracker import save_weather_to_csv
from features.compare_cities import compare_cities_from_csv
from src.gui_icons import GUIIcons

class TabbedWeatherApp:
    """
    Tabbed Weather Dashboard with multiple features
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather Dashboard - Dunasha Payne")
        self.root.geometry("600x500")
        
        self.weather_service = WeatherService()
        self.settings = SettingsManager()
        
        self.setup_tabs()
        
    def setup_tabs(self):
        """Create the tab interface"""
        notebook = ttk.Notebook(self.root)
        
        # Tab 1: Main Weather Search
        self.main_tab = ttk.Frame(notebook)
        notebook.add(self.main_tab, text="Weather Search")
        self.setup_main_tab()
        
        # Tab 2: City Comparison
        self.compare_tab = ttk.Frame(notebook)
        notebook.add(self.compare_tab, text="Compare Cities")
        self.setup_compare_tab()
        
        # Tab 3: Weather History
        self.history_tab = ttk.Frame(notebook)
        notebook.add(self.history_tab, text="Search History")
        self.setup_history_tab()
        
        notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
    def setup_main_tab(self):
        """Setup the main weather search tab"""
        # Title
        title_label = tk.Label(self.main_tab, text="Weather Search", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # City input frame
        input_frame = tk.Frame(self.main_tab)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Enter City Name:").pack(side=tk.LEFT, padx=5)
        self.city_entry = tk.Entry(input_frame, width=25, font=('Arial', 12))
        self.city_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(input_frame, text="Get Weather", 
                              command=self.search_weather,
                              bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Weather display frame
        self.weather_frame = tk.Frame(self.main_tab, relief=tk.RIDGE, bd=2)
        self.weather_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.weather_display = tk.Label(self.weather_frame, text="Enter a city name to get weather information",
                                       font=('Arial', 11), justify=tk.LEFT, wraplength=500)
        self.weather_display.pack(pady=20)
        
        # Load last searched city
        last_city = self.settings.get_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)
            
    def setup_compare_tab(self):
        """Setup the city comparison tab"""
        title_label = tk.Label(self.compare_tab, text="Compare Two Cities", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Input frame for two cities
        input_frame = tk.Frame(self.compare_tab)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="City 1:").grid(row=0, column=0, padx=5, pady=5)
        self.city1_entry = tk.Entry(input_frame, width=20, font=('Arial', 12))
        self.city1_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="City 2:").grid(row=1, column=0, padx=5, pady=5)
        self.city2_entry = tk.Entry(input_frame, width=20, font=('Arial', 12))
        self.city2_entry.grid(row=1, column=1, padx=5, pady=5)
        
        compare_btn = tk.Button(input_frame, text="Compare Cities", 
                               command=self.compare_cities,
                               bg='#2196F3', fg='white', font=('Arial', 10, 'bold'))
        compare_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Comparison results frame
        self.compare_frame = tk.Frame(self.compare_tab, relief=tk.RIDGE, bd=2)
        self.compare_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.compare_display = tk.Label(self.compare_frame, 
                                       text="Enter two city names to compare their weather",
                                       font=('Arial', 11), justify=tk.LEFT, wraplength=500)
        self.compare_display.pack(pady=20)
        
    def setup_history_tab(self):
        """Setup the search history tab"""
        title_label = tk.Label(self.history_tab, text="Recent Weather Searches", 
                              font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # History display frame
        self.history_frame = tk.Frame(self.history_tab, relief=tk.RIDGE, bd=2)
        self.history_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # Scrollable text widget for history
        scrollbar = tk.Scrollbar(self.history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(self.history_frame, wrap=tk.WORD, 
                                   yscrollcommand=scrollbar.set,
                                   font=('Arial', 10))
        self.history_text.pack(side=tk.LEFT, fill='both', expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Refresh button
        refresh_btn = tk.Button(self.history_tab, text="Refresh History", 
                               command=self.load_history,
                               bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        refresh_btn.pack(pady=10)
        
        # Load history on startup
        self.load_history()
        
    def search_weather(self):
        """Search weather for a single city"""
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name.")
            return
            
        try:
            weather_data = self.weather_service.get_weather_data(city_name)
            if weather_data:
                self.settings.set_last_city(city_name)
                
                # Get weather icon
                icon = GUIIcons.get_icon(weather_data['description'], 
                                       weather_data['temperature'])
                
                # Update display
                weather_text = (
                    f"{icon} Weather in {weather_data['city']}\n\n"
                    f"🌡️ Temperature: {weather_data['temperature']}°C\n"
                    f"📝 Description: {weather_data['description'].title()}\n"
                    f"💧 Humidity: {weather_data['humidity']}%\n"
                    f"💨 Wind Speed: {weather_data['wind_speed']} m/s"
                )
                self.weather_display.config(text=weather_text)
                
                # Save to CSV
                save_weather_to_csv(
                    weather_data['city'],
                    weather_data['temperature'],
                    weather_data['description']
                )
                
            else:
                messagebox.showerror("Error", "Could not fetch weather data. Please check the city name.")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            
    def compare_cities(self):
        """Compare weather between two cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showerror("Error", "Please enter both city names.")
            return
            
        try:
            comparison_result = compare_cities_from_csv(city1, city2)
            self.compare_display.config(text=comparison_result)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            
    def load_history(self):
        """Load and display weather search history"""
        try:
            # Use the actual team weather CSV file
            history_file = os.path.join(os.path.dirname(__file__), "..", "data", "team_weather.csv")
            self.history_text.delete(1.0, tk.END)
            
            if not os.path.exists(history_file):
                self.history_text.insert(tk.END, "No search history found.")
                return
                
            with open(history_file, 'r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
            if not rows:
                self.history_text.insert(tk.END, "No search history found.")
                return
                
            self.history_text.insert(tk.END, "Recent Weather Searches:\n")
            self.history_text.insert(tk.END, "=" * 40 + "\n\n")
            
            # Show last 10 searches
            recent_searches = rows[-10:] if len(rows) > 10 else rows
            
            for row in reversed(recent_searches):
                city = row.get('city', row.get('City', 'Unknown'))
                timestamp = row.get('timestamp', row.get('Timestamp', 'Unknown'))
                temp = row.get('temperature', row.get('Temperature (F)', 'N/A'))
                condition = row.get('weather_description', row.get('Description', 'N/A'))
                
                icon = GUIIcons.get_icon(condition)
                
                entry = (f"{icon} {city}\n"
                       f"   🗓️ {timestamp}\n"
                       f"   🌡️ {temp}°F - {condition.title()}\n\n")
                
                self.history_text.insert(tk.END, entry)
                    
        except Exception as e:
            self.history_text.delete(1.0, tk.END)
            self.history_text.insert(tk.END, f"Error loading history: {e}")
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = TabbedWeatherApp()
    app.run()

if __name__ == "__main__":
    main()
