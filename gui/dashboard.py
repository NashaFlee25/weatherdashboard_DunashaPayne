"""
Weather Dashboard GUI application using Tkinter.
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Optional, List, Dict, Any
import requests
import json
import logging
import os
from datetime import datetime

# Import data functions
from data.io import write_weather_record, read_weather_records, calculate_weather_statistics

# Self-contained implementations to avoid missing imports
class WeatherService:
    """Simple weather service using OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = "your_api_key_here"  # Replace with actual API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_data(self, city: str) -> Optional[Dict[str, Any]]:
        """Get weather data for a city."""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data['name'],
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed']
                }
        except Exception as e:
            logging.error(f"Weather API error: {e}")
        return None

class SettingsManager:
    """Simple settings manager using JSON file."""
    
    def __init__(self):
        self.settings_file = "settings.json"
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_settings(self) -> None:
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except Exception:
            pass
    
    def get_last_city(self) -> Optional[str]:
        """Get the last searched city."""
        return self.settings.get('last_city')
    
    def set_last_city(self, city: str) -> None:
        """Set the last searched city."""
        self.settings['last_city'] = city
        self._save_settings()
    
    def get_user_name(self) -> Optional[str]:
        """Get the user name."""
        return self.settings.get('user_name')
    
    def set_user_name(self, name: str) -> None:
        """Set the user name."""
        self.settings['user_name'] = name
        self._save_settings()

class GUIIcons:
    """Simple weather icons."""
    
    @staticmethod
    def get_icon(description: str, temperature: float) -> str:
        """Get weather icon based on description."""
        description = description.lower()
        if 'clear' in description:
            return "☀️"
        elif 'cloud' in description:
            return "☁️"
        elif 'rain' in description:
            return "🌧️"
        elif 'snow' in description:
            return "❄️"
        elif 'thunder' in description:
            return "⛈️"
        else:
            return "🌤️"

# Utility functions
def get_personalized_greeting(name: str) -> str:
    """Get personalized greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    return f"{greeting}, {name}! Welcome to Weather Dashboard"

def get_weather_phrase(description: str) -> str:
    """Get weather phrase."""
    return f"It's {description} outside!"

def suggest_activity(temp: float, desc: str) -> str:
    """Suggest activity based on weather."""
    if temp > 25:
        return "Perfect weather for outdoor activities!"
    elif temp < 10:
        return "Great weather to stay cozy indoors!"
    else:
        return "Nice weather for a walk!"

def setup_logger():
    """Set up logger."""
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)

# Constants
WINDOW_TITLE = "Weather Dashboard"
WINDOW_SIZE = "800x600"
THEMES = {
    "Light": {"bg": "#ffffff", "fg": "#000000"},
    "Dark": {"bg": "#2b2b2b", "fg": "#ffffff"}
}
DEFAULT_HISTORY_ENTRIES = 10


class WeatherDashboard:
    """
    Weather Dashboard GUI application using Tkinter.
    """
    
    def __init__(self):
        """Initialize the weather dashboard application."""
        self.logger = setup_logger()
        self.weather_service = WeatherService()
        self.settings = SettingsManager()
        self.root = tk.Tk()
        self.result_text = tk.StringVar()
        self.icon_text = tk.StringVar()
        self.gui_elements: List[tk.Widget] = []
        self._setup_gui()

    def _setup_gui(self) -> None:
        """Set up the main GUI components with tabbed layout."""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        
        # Configure ttk style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure root grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Get user name and create personalized greeting
        user_name = self._get_user_name()
        greeting_text = get_personalized_greeting(user_name)
        self.greeting_label = ttk.Label(self.root, text=greeting_text, font=("Arial", 12, "bold"))
        self.greeting_label.grid(row=0, column=0, pady=5, sticky="ew")
        self.gui_elements.append(self.greeting_label)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create frames for each tab
        self.weather_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)
        self.stats_frame = ttk.Frame(self.notebook)
        self.settings_frame = ttk.Frame(self.notebook)
        
        # Add tabs to notebook
        self.notebook.add(self.weather_frame, text="Weather")
        self.notebook.add(self.history_frame, text="History")
        self.notebook.add(self.stats_frame, text="Stats")
        self.notebook.add(self.settings_frame, text="Settings")
        
        # Configure frame grids
        for frame in [self.weather_frame, self.history_frame, self.stats_frame, self.settings_frame]:
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.rowconfigure(0, weight=1)
        
        self._setup_weather_tab()
        self._setup_history_tab()
        self._setup_stats_tab()
        self._setup_settings_tab()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_weather_tab(self) -> None:
        """Set up the weather tab components."""
        # City input
        city_label = ttk.Label(self.weather_frame, text="Enter City Name:")
        city_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.gui_elements.append(city_label)

        self.city_entry = ttk.Entry(self.weather_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.gui_elements.append(self.city_entry)

        # Get Weather button
        get_weather_btn = ttk.Button(self.weather_frame, text="Get Weather", command=self.display_weather)
        get_weather_btn.grid(row=1, column=0, columnspan=2, pady=10)
        self.gui_elements.append(get_weather_btn)

        # Weather display area
        display_frame = ttk.Frame(self.weather_frame)
        display_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Weather icon
        self.icon_label = ttk.Label(display_frame, textvariable=self.icon_text, font=("Arial", 32))
        self.icon_label.grid(row=0, column=0, padx=10, pady=10)
        self.gui_elements.append(self.icon_label)

        # Weather result
        self.result_label = ttk.Label(display_frame, textvariable=self.result_text, justify="left", wraplength=400)
        self.result_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.gui_elements.append(self.result_label)

        # Load last city
        last_city = self.settings.get_last_city()
        if last_city:
            self.city_entry.insert(0, last_city)

    def _setup_history_tab(self) -> None:
        """Set up the history tab components."""
        # History button
        history_btn = ttk.Button(self.history_frame, text="View History", command=self.show_history)
        history_btn.grid(row=0, column=0, columnspan=2, pady=20)
        self.gui_elements.append(history_btn)
        
        # Placeholder for future history display
        history_info = ttk.Label(self.history_frame, text="Click 'View History' to see recent weather data", 
                                font=("Arial", 10), foreground="gray")
        history_info.grid(row=1, column=0, columnspan=2, pady=10)
        self.gui_elements.append(history_info)

    def _setup_stats_tab(self) -> None:
        """Set up the stats tab components."""
        # Stats button
        stats_btn = ttk.Button(self.stats_frame, text="Show Stats", command=self.display_stats)
        stats_btn.grid(row=0, column=0, columnspan=2, pady=20)
        self.gui_elements.append(stats_btn)
        
        # Placeholder for future stats display
        stats_info = ttk.Label(self.stats_frame, text="Click 'Show Stats' to view weather statistics", 
                              font=("Arial", 10), foreground="gray")
        stats_info.grid(row=1, column=0, columnspan=2, pady=10)
        self.gui_elements.append(stats_info)

    def _setup_settings_tab(self) -> None:
        """Set up the settings tab components."""        
        # Theme selection
        theme_label = ttk.Label(self.settings_frame, text="Theme:")
        theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.gui_elements.append(theme_label)

        self.theme_var = tk.StringVar(value="Light")
        theme_combo = ttk.Combobox(self.settings_frame, textvariable=self.theme_var, 
                                  values=list(THEMES.keys()), state="readonly")
        theme_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        theme_combo.bind('<<ComboboxSelected>>', lambda e: self.apply_theme(self.theme_var.get()))
        self.gui_elements.append(theme_combo)

        # Change name button
        change_name_btn = ttk.Button(self.settings_frame, text="Change Name", command=self.change_user_name)
        change_name_btn.grid(row=1, column=0, columnspan=2, pady=20)
        self.gui_elements.append(change_name_btn)
        
        # Apply initial theme
        self.apply_theme(self.theme_var.get())

    def apply_theme(self, selected: str) -> None:
        """Apply the chosen theme colors to the window and all child widgets."""        
        style_config = THEMES.get(selected, THEMES["Light"])
        bg, fg = style_config["bg"], style_config["fg"]

        # Configure root window
        self.root.configure(bg=bg)

        # Configure ttk styles for the selected theme
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('TNotebook', background=bg, borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=bg, 
                       foreground=fg,
                       padding=[10, 5],
                       focuscolor='none')
        style.map('TNotebook.Tab',
                 background=[('selected', bg), ('active', bg)],
                 foreground=[('selected', fg), ('active', fg)])
        
        # Configure frame style
        style.configure('TFrame', background=bg)
        
        # Configure label style
        style.configure('TLabel', background=bg, foreground=fg)
        
        # Configure button style
        style.configure('TButton', 
                       background=bg, 
                       foreground=fg,
                       focuscolor='none')
        style.map('TButton',
                 background=[('active', bg), ('pressed', bg)],
                 foreground=[('active', fg), ('pressed', fg)])
        
        # Configure entry style
        style.configure('TEntry', 
                       fieldbackground=bg, 
                       foreground=fg,
                       bordercolor=fg,
                       insertcolor=fg)
        
        # Configure combobox style
        style.configure('TCombobox', 
                       fieldbackground=bg, 
                       foreground=fg,
                       bordercolor=fg,
                       selectbackground=bg,
                       selectforeground=fg)
        style.map('TCombobox',
                 fieldbackground=[('readonly', bg)],
                 selectbackground=[('readonly', bg)])

        # Apply theme to all frames
        for frame in [self.weather_frame, self.history_frame, self.stats_frame, self.settings_frame]:
            self._apply_theme_to_frame(frame, bg, fg)

    def _apply_theme_to_frame(self, frame: tk.Widget, bg: str, fg: str) -> None:
        """Recursively apply theme to all widgets in a frame."""
        for widget in frame.winfo_children():
            widget_class = widget.__class__.__name__
            
            # Handle different widget types
            if widget_class in ['Frame', 'Toplevel']:
                try:
                    widget.configure(bg=bg)
                    # Recursively apply to children
                    self._apply_theme_to_frame(widget, bg, fg)
                except tk.TclError:
                    pass
            elif widget_class in ['Label', 'Button']:
                try:
                    widget.configure(bg=bg, fg=fg)
                except tk.TclError:
                    pass
            elif widget_class == 'Entry':
                try:
                    widget.configure(bg=bg, fg=fg, insertbackground=fg)
                except tk.TclError:
                    pass
            elif widget_class == 'Text':
                try:
                    widget.configure(bg=bg, fg=fg, insertbackground=fg)
                except tk.TclError:
                    pass
            elif widget_class == 'Scrollbar':
                try:
                    widget.configure(bg=bg, troughcolor=bg, activebackground=fg)
                except tk.TclError:
                    pass

    def display_weather(self) -> None:
        """Fetch and display weather data for the entered city."""
        city_name = self.city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        
        try:
            weather_data = self.weather_service.get_weather_data(city_name)
        except Exception as e:
            self.logger.error(f"Failed to fetch weather data: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
            return

        if weather_data:
            self.settings.set_last_city(city_name)
            self._update_display(weather_data)
        else:
            messagebox.showerror("Error", "Could not fetch weather data. Please try again.")

    def _update_display(self, weather_data: Dict[str, Any]) -> None:
        """Update the result label, weather icon, and save weather data to CSV."""
        # Get icon for current weather with error handling
        try:
            if hasattr(GUIIcons, 'get_icon'):
                icon = GUIIcons.get_icon(weather_data.get('description', ''), weather_data.get('temperature'))
            else:
                icon = "🌤️"  # Default weather icon
        except Exception:
            icon = "🌤️"  # Fallback icon on any error
            
        self.icon_text.set(icon)
        
        phrase = get_weather_phrase(weather_data["description"])
        activity = suggest_activity(weather_data["temperature"], weather_data["description"])
        
        self.result_text.set(
            f"Weather in {weather_data['city']}:\n"
            f"Temperature: {weather_data['temperature']}°C\n"
            f"Description: {weather_data['description']}\n"
            f"Humidity: {weather_data['humidity']}%\n"
            f"Wind Speed: {weather_data['wind_speed']} m/s\n"
            f"{phrase}\n{activity}"
        )
        
        try:
            write_weather_record(
                weather_data['city'],
                weather_data['temperature'],
                weather_data['description']
            )
        except Exception as e:
            self.logger.error(f"Failed to save weather data: {e}")
            messagebox.showerror("Error", f"Failed to save weather data: {e}")

    def show_history(self) -> None:
        """Display a window showing the last 10 weather entries."""
        history_entries = read_weather_records(DEFAULT_HISTORY_ENTRIES)
        
        if not history_entries:
            messagebox.showinfo("History", "No weather history found.")
            return
        
        # Create history window
        history_window = tk.Toplevel(self.root)
        history_window.title("Weather History")
        history_window.geometry("400x300")
        
        # Create scrollable text widget
        text_frame = tk.Frame(history_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_text = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_text.yview)
        
        # Display history entries
        history_text.insert(tk.END, "Recent Weather History:\n\n")
        for i, entry in enumerate(reversed(history_entries), 1):
            history_text.insert(tk.END, 
                f"{i}. {entry['City']}\n"
                f"   Temperature: {entry['Temperature']}°C\n"
                f"   Description: {entry['Description']}\n\n"
            )
        
        history_text.config(state=tk.DISABLED)  # Make read-only

    def display_stats(self) -> None:
        """Display weather statistics from CSV data."""
        stats = calculate_weather_statistics()
        
        if stats["min"] is None:
            messagebox.showinfo("Weather Stats", "No weather data available for statistics.")
            return
        
        # Build message string
        message = f"Weather Statistics:\n\n"
        message += f"Temperature Range:\n"
        message += f"  Minimum: {stats['min']:.1f}°C\n"
        message += f"  Maximum: {stats['max']:.1f}°C\n\n"
        
        if stats["counts"]:
            message += "Weather Descriptions:\n"
            for description, count in stats["counts"].items():
                message += f"  {description}: {count}\n"
        
        messagebox.showinfo("Weather Stats", message)

    def _on_close(self) -> None:
        """Handle application close event."""
        self.root.destroy()

    def _get_user_name(self) -> str:
        """Get user name from settings or prompt for input."""        
        user_name = None
        
        # Try to get user name from settings with error handling
        try:
            if hasattr(self.settings, 'get_user_name'):
                user_name = self.settings.get_user_name()
        except Exception:
            user_name = None
            
        if not user_name:
            user_name = self._prompt_for_name()
            if user_name:
                # Try to save user name with error handling
                try:
                    if hasattr(self.settings, 'set_user_name'):
                        self.settings.set_user_name(user_name)
                except Exception:
                    pass  # Continue without saving if method doesn't exist
            else:
                user_name = "User"  # Default fallback
        return user_name

    def _prompt_for_name(self) -> Optional[str]:
        """Prompt user to enter their name."""
        return simpledialog.askstring(
            "Welcome!",
            "What's your name?",
            parent=self.root
        )

    def change_user_name(self) -> None:
        """Allow user to change their name and update greeting."""
        new_name = self._prompt_for_name()
        if new_name:
            # Try to save user name with error handling
            try:
                if hasattr(self.settings, 'set_user_name'):
                    self.settings.set_user_name(new_name)
            except Exception:
                pass  # Continue without saving if method doesn't exist
                
            # Update greeting with new name
            greeting_text = get_personalized_greeting(new_name)
            self.greeting_label.config(text=greeting_text)

    def run(self) -> None:
        """Start the GUI application."""        
        self.root.mainloop()
