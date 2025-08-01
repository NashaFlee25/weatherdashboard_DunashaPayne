"""Main application window."""

import tkinter as tk
from tkinter import ttk
import asyncio
import threading
from typing import Optional

from src.presentation.views.weather_view import WeatherDisplayView, WeatherSearchView, WeatherComparisonView
from src.presentation.controllers.weather_controller import WeatherController
from src.infrastructure.config.settings import UIConfig
from src.domain.interfaces import ISettingsRepository


class MainWindow:
    """Main application window."""
    
    def __init__(self, weather_controller: WeatherController, 
                 settings_repo: ISettingsRepository,
                 ui_config: UIConfig):
        self.weather_controller = weather_controller
        self.settings_repo = settings_repo
        self.ui_config = ui_config
        self.root: Optional[tk.Tk] = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        
    def create_window(self) -> tk.Tk:
        """Create and configure the main window."""
        self.root = tk.Tk()
        self.root.title("Weather Dashboard")
        self.root.geometry(f"{self.ui_config.window_width}x{self.ui_config.window_height}")
        self.root.minsize(800, 600)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self._create_widgets()
        self._setup_async_loop()
        
        # Load last searched city if available
        last_city = self.settings_repo.get_last_searched_city()
        if last_city and self.search_view:
            self.search_view.set_city(last_city)
        
        return self.root
    
    def _create_widgets(self):
        """Create and arrange widgets."""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill="both", expand=True)
        
        # Search tab
        search_tab = ttk.Frame(notebook)
        notebook.add(search_tab, text="Weather Search")
        
        self.search_view = WeatherSearchView(search_tab, self.weather_controller.search_weather)
        self.display_view = WeatherDisplayView(search_tab)
        
        # Comparison tab
        comparison_tab = ttk.Frame(notebook)
        notebook.add(comparison_tab, text="Compare Cities")
        
        self.comparison_view = WeatherComparisonView(comparison_tab, self.weather_controller.compare_cities)
        self.comparison_display_view = WeatherDisplayView(comparison_tab)
        
        # Set views in controller
        self.weather_controller.set_views(
            self.display_view, 
            self.search_view, 
            self.comparison_view
        )
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief="sunken")
        status_bar.pack(side="bottom", fill="x", pady=(5, 0))
    
    def _setup_async_loop(self):
        """Setup asyncio event loop for the GUI."""
        def run_async_loop():
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        
        # Start the async loop in a separate thread
        async_thread = threading.Thread(target=run_async_loop, daemon=True)
        async_thread.start()
    
    def run(self):
        """Start the application."""
        if self.root:
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            self.root.mainloop()
    
    def _on_closing(self):
        """Handle window closing."""
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        if self.root:
            self.root.destroy()
