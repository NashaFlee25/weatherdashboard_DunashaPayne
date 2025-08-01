import json
import os
import tkinter as tk
from tkinter import ttk

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.config_file = os.path.join(os.path.dirname(__file__), "..", "data", "theme_config.json")
        
        # Define theme colors
        self.themes = {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "select_bg": "#0078d4",
                "select_fg": "#ffffff",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "button_bg": "#f0f0f0",
                "button_fg": "#000000",
                "button_active_bg": "#e0e0e0"
            },
            "dark": {
                "bg": "#2b2b2b",
                "fg": "#ffffff",
                "select_bg": "#404040",
                "select_fg": "#ffffff",
                "entry_bg": "#404040",
                "entry_fg": "#ffffff",
                "button_bg": "#404040",
                "button_fg": "#ffffff",
                "button_active_bg": "#505050"
            }
        }
        
        self.current_theme = self.load_theme_preference()
        self.widgets_to_theme = []
    
    def load_theme_preference(self):
        """Load theme preference from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('theme', 'light')
        except Exception:
            pass
        return 'light'
    
    def save_theme_preference(self):
        """Save current theme preference to config file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            config = {'theme': self.current_theme}
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def register_widget(self, widget, widget_type="default"):
        """Register a widget to be themed"""
        self.widgets_to_theme.append((widget, widget_type))
    
    def apply_theme(self, theme_name=None):
        """Apply the specified theme to all registered widgets"""
        if theme_name:
            self.current_theme = theme_name
        
        theme = self.themes[self.current_theme]
        
        # Apply theme to root window
        self.root.configure(bg=theme["bg"])
        
        # Apply theme to all registered widgets
        for widget, widget_type in self.widgets_to_theme:
            try:
                if widget_type == "entry":
                    widget.configure(
                        bg=theme["entry_bg"],
                        fg=theme["entry_fg"],
                        insertbackground=theme["entry_fg"]
                    )
                elif widget_type == "button":
                    widget.configure(
                        bg=theme["button_bg"],
                        fg=theme["button_fg"],
                        activebackground=theme["button_active_bg"],
                        activeforeground=theme["button_fg"]
                    )
                elif widget_type == "text":
                    widget.configure(
                        bg=theme["bg"],
                        fg=theme["fg"],
                        insertbackground=theme["fg"],
                        selectbackground=theme["select_bg"],
                        selectforeground=theme["select_fg"]
                    )
                else:  # labels and other widgets
                    widget.configure(
                        bg=theme["bg"],
                        fg=theme["fg"]
                    )
            except tk.TclError:
                # Some widgets might not support all configuration options
                pass
        
        self.save_theme_preference()
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme(new_theme)
        return new_theme
    
    def create_theme_toggle_button(self, parent):
        """Create a theme toggle button"""
        def on_toggle():
            new_theme = self.toggle_theme()
            button.configure(text=f"🌙 Dark Mode" if new_theme == "light" else "☀️ Light Mode")
        
        button_text = "🌙 Dark Mode" if self.current_theme == "light" else "☀️ Light Mode"
        button = tk.Button(
            parent,
            text=button_text,
            command=on_toggle,
            font=("Arial", 10)
        )
        
        self.register_widget(button, "button")
        return button
