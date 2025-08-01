"""Dropdown UI components for city selection interface."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional
from services.city_data_loader import CityDataLoader


class WeatherComparisonUI:
    """UI component for weather comparison with city selection dropdowns."""
    
    def __init__(self, parent_frame: ttk.Frame, city_loader: CityDataLoader):
        """
        Initialize the weather comparison UI.
        
        Args:
            parent_frame (ttk.Frame): Parent frame to contain this UI
            city_loader (CityDataLoader): Service for loading city data
        """
        self.parent_frame = parent_frame
        self.city_loader = city_loader
        
        # StringVar objects to hold selected cities
        self.selected_city1 = tk.StringVar()
        self.selected_city2 = tk.StringVar()
        
        # UI components
        self.city1_dropdown: Optional[ttk.Combobox] = None
        self.city2_dropdown: Optional[ttk.Combobox] = None
        
        # Build the UI
        self._create_ui()
    
    def _create_ui(self) -> None:
        """Create the user interface components."""
        # Main comparison frame
        self.comparison_frame = ttk.LabelFrame(
            self.parent_frame,
            text="City Weather Comparison",
            padding="15"
        )
        self.comparison_frame.pack(fill="x", padx=10, pady=10)
        
        # Create dropdown section
        self._create_dropdown_section()
        
        # Create control buttons
        self._create_control_buttons()
    
    def _create_dropdown_section(self) -> None:
        """Create the dropdown selection section."""
        dropdown_frame = ttk.Frame(self.comparison_frame)
        dropdown_frame.pack(fill="x", pady=(0, 10))
        
        # City 1 selection
        city1_frame = ttk.LabelFrame(dropdown_frame, text="Select First City", padding="10")
        city1_frame.pack(side="left", padx=(0, 10), fill="both", expand=True)
        
        self.city1_dropdown = ttk.Combobox(
            city1_frame,
            textvariable=self.selected_city1,
            values=self.city_loader.get_city_names(),
            state="readonly",
            width=25
        )
        self.city1_dropdown.pack(pady=5)
        self.city1_dropdown.bind('<<ComboboxSelected>>', self._on_city1_selected)
        
        # City 2 selection  
        city2_frame = ttk.LabelFrame(dropdown_frame, text="Select Second City", padding="10")
        city2_frame.pack(side="right", padx=(10, 0), fill="both", expand=True)
        
        self.city2_dropdown = ttk.Combobox(
            city2_frame,
            textvariable=self.selected_city2,
            values=self.city_loader.get_city_names(),
            state="readonly",
            width=25
        )
        self.city2_dropdown.pack(pady=5)
        self.city2_dropdown.bind('<<ComboboxSelected>>', self._on_city2_selected)
    
    def _create_control_buttons(self) -> None:
        """Create control buttons for the UI."""
        button_frame = ttk.Frame(self.comparison_frame)
        button_frame.pack(fill="x")
        
        # Refresh cities button
        refresh_btn = ttk.Button(
            button_frame,
            text="Refresh City List",
            command=self._refresh_city_data
        )
        refresh_btn.pack(side="left")
        
        # Clear selections button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Selections",
            command=self._clear_selections
        )
        clear_btn.pack(side="left", padx=(10, 0))
        
        # City count label
        city_count = self.city_loader.get_city_count()
        self.count_label = ttk.Label(
            button_frame,
            text=f"Cities available: {city_count}"
        )
        self.count_label.pack(side="right")
    
    def _on_city1_selected(self, event) -> None:
        """
        Handle City 1 dropdown selection.
        
        Args:
            event: Tkinter event object
        """
        selected_city = self.selected_city1.get()
        print(f"City 1 selected: {selected_city}")
        
        # Validate selection
        if not self.city_loader.is_valid_city(selected_city):
            print(f"Warning: {selected_city} is not a valid city")
    
    def _on_city2_selected(self, event) -> None:
        """
        Handle City 2 dropdown selection.
        
        Args:
            event: Tkinter event object
        """
        selected_city = self.selected_city2.get()
        print(f"City 2 selected: {selected_city}")
        
        # Validate selection
        if not self.city_loader.is_valid_city(selected_city):
            print(f"Warning: {selected_city} is not a valid city")
    
    def _refresh_city_data(self) -> None:
        """Refresh city data from CSV and update dropdowns."""
        self.city_loader.refresh_cities()
        city_names = self.city_loader.get_city_names()
        
        # Update dropdown values
        if self.city1_dropdown:
            self.city1_dropdown['values'] = city_names
        if self.city2_dropdown:
            self.city2_dropdown['values'] = city_names
        
        # Update count label
        city_count = self.city_loader.get_city_count()
        self.count_label.config(text=f"Cities available: {city_count}")
        
        print(f"City data refreshed. {city_count} cities available.")
    
    def _clear_selections(self) -> None:
        """Clear both city selections."""
        self.selected_city1.set("")
        self.selected_city2.set("")
        print("City selections cleared")
    
    def get_selected_cities(self) -> Dict[str, str]:
        """
        Get the currently selected cities.
        
        Returns:
            Dict[str, str]: Dictionary with 'city1' and 'city2' keys
        """
        return {
            'city1': self.selected_city1.get(),
            'city2': self.selected_city2.get()
        }
    
    def set_selected_cities(self, city1: Optional[str] = None, city2: Optional[str] = None) -> None:
        """
        Programmatically set selected cities.
        
        Args:
            city1 (Optional[str]): Name of first city to select
            city2 (Optional[str]): Name of second city to select
        """
        if city1 and self.city_loader.is_valid_city(city1):
            self.selected_city1.set(city1)
        
        if city2 and self.city_loader.is_valid_city(city2):
            self.selected_city2.set(city2)
