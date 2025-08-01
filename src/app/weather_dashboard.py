"""Weather Dashboard Application - Main Application Class."""

import tkinter as tk
from tkinter import ttk, messagebox

from src.gui.dropdown_ui import WeatherComparisonUI
from src.gui.charts import ChartManager
from src.services.city_data_loader import CityDataLoader
from src.utils.dependencies import DependencyChecker


class WeatherDashboardApp:
    """Main application class for the Weather Dashboard."""
    
    def __init__(self):
        """Initialize the main application."""
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry("1200x800")
        
        # Initialize services
        self.city_loader = CityDataLoader("data/team_weather.csv")
        self.chart_manager = ChartManager()
        self.dependency_checker = DependencyChecker()
        
        # Create UI
        self._setup_main_frame()
        self._setup_ui_components()
        
        # Check dependencies
        self.dependency_checker.show_warnings()
    
    def _setup_main_frame(self):
        """Create the main scrollable frame."""
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
    
    def _setup_ui_components(self):
        """Set up the user interface components."""
        # Title
        title_label = ttk.Label(
            self.scrollable_frame, 
            text="Weather Dashboard", 
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=20)
        
        # Weather comparison UI
        self.weather_comparison_ui = WeatherComparisonUI(
            parent_frame=self.scrollable_frame,
            city_loader=self.city_loader
        )
        
        # Control buttons
        self._create_control_buttons()
        
        # Results frame
        self.results_frame = ttk.Frame(self.scrollable_frame)
        self.results_frame.pack(fill="both", expand=True, pady=20)
        
        # Status bar
        self._create_status_bar()
    
    def _create_control_buttons(self):
        """Create control buttons."""
        control_frame = ttk.Frame(self.scrollable_frame)
        control_frame.pack(pady=20, fill="x")
        
        buttons = [
            ("Compare Cities", self.compare_cities),
            ("Show Statistics", self.show_statistics),
            ("Weather Trends", self.show_weather_trends),
            ("Current Weather", self.show_current_weather)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(control_frame, text=text, command=command)
            btn.pack(side="left", padx=5)
            
            # Disable trends button if matplotlib not available
            if text == "Weather Trends" and not self.dependency_checker.has_matplotlib:
                btn.config(state="disabled")
    
    def _create_status_bar(self):
        """Create status bar."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select cities to compare weather data")
        status_bar = ttk.Label(self.scrollable_frame, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
    
    def compare_cities(self):
        """Compare weather data between selected cities."""
        selected_cities = self.weather_comparison_ui.get_selected_cities()
        
        if not self._validate_city_selection(selected_cities, require_both=True):
            return
        
        self._clear_results()
        
        city1_data = self.city_loader.get_weather_data(selected_cities['city1'])
        city2_data = self.city_loader.get_weather_data(selected_cities['city2'])
        
        if not self._validate_city_data(city1_data, city2_data):
            return
        
        # Create comparison visualization
        self.chart_manager.create_comparison_display(
            self.results_frame, city1_data, city2_data, selected_cities
        )
        
        self.status_var.set(f"Comparing {selected_cities['city1']} with {selected_cities['city2']}")
    
    def show_statistics(self):
        """Display weather statistics for selected cities."""
        selected_cities = self.weather_comparison_ui.get_selected_cities()
        
        if not self._validate_city_selection(selected_cities):
            return
        
        self._clear_results()
        
        stats_frame = ttk.LabelFrame(self.results_frame, text="Weather Statistics")
        stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for city_key, city_name in selected_cities.items():
            if city_name:
                city_data = self.city_loader.get_weather_data(city_name)
                if city_data is not None:
                    self.chart_manager.display_city_stats(stats_frame, city_name, city_data)
        
        self.status_var.set("Statistics displayed")
    
    def show_weather_trends(self):
        """Show weather trends over time."""
        if not self.dependency_checker.has_matplotlib:
            messagebox.showwarning("Feature Unavailable", 
                                 "Weather trends require matplotlib. Please install matplotlib to use this feature.")
            return
        
        selected_cities = self.weather_comparison_ui.get_selected_cities()
        
        if not self._validate_city_selection(selected_cities):
            return
        
        self._clear_results()
        
        self.chart_manager.create_trends_chart(self.results_frame, selected_cities, self.city_loader)
        self.status_var.set("Weather trends displayed")
    
    def show_current_weather(self):
        """Display current weather conditions."""
        selected_cities = self.weather_comparison_ui.get_selected_cities()
        
        if not self._validate_city_selection(selected_cities):
            return
        
        self._clear_results()
        
        current_frame = ttk.LabelFrame(self.results_frame, text="Current Weather Conditions")
        current_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for city_key, city_name in selected_cities.items():
            if city_name:
                city_data = self.city_loader.get_weather_data(city_name)
                if city_data is not None:
                    self.chart_manager.display_current_weather(current_frame, city_name, city_data)
        
        self.status_var.set("Current weather displayed")
    
    def _validate_city_selection(self, selected_cities, require_both=False):
        """Validate city selection."""
        if require_both:
            if not (selected_cities['city1'] and selected_cities['city2']):
                self.status_var.set("Please select both cities for comparison")
                return False
        else:
            if not (selected_cities['city1'] or selected_cities['city2']):
                self.status_var.set("Please select at least one city")
                return False
        return True
    
    def _validate_city_data(self, city1_data, city2_data):
        """Validate city data."""
        if city1_data is None or city2_data is None:
            self.status_var.set("Error loading city data")
            return False
        return True
    
    def _clear_results(self):
        """Clear the results frame."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def run(self):
        """Start the application main loop."""
        self.root.mainloop()
