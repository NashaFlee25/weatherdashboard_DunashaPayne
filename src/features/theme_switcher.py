"""Theme switcher feature implementation."""

import tkinter as tk
from tkinter import ttk
import json
import os


class ThemeSwitcher:
    """Feature for switching between light and dark themes."""
    
    def __init__(self, root):
        """Initialize theme switcher."""
        self.root = root
        self.current_theme = 'light'
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'button_bg': '#f0f0f0',
                'button_fg': '#000000'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'select_bg': '#404040',
                'select_fg': '#ffffff',
                'entry_bg': '#404040',
                'entry_fg': '#ffffff',
                'button_bg': '#505050',
                'button_fg': '#ffffff'
            },
            'blue': {
                'bg': '#e6f3ff',
                'fg': '#000080',
                'select_bg': '#0066cc',
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#000080',
                'button_bg': '#cce6ff',
                'button_fg': '#000080'
            },
            'nature': {
                'bg': '#f0f8e6',
                'fg': '#2d4a2d',
                'select_bg': '#4d7a4d',
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#2d4a2d',
                'button_bg': '#d9f2d9',
                'button_fg': '#2d4a2d'
            }
        }
        
        self.load_theme_preference()
        self.apply_theme()
    
    def toggle_theme(self):
        """Toggle between available themes."""
        theme_list = list(self.themes.keys())
        current_index = theme_list.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_list)
        
        self.current_theme = theme_list[next_index]
        self.apply_theme()
        self.save_theme_preference()
    
    def set_theme(self, theme_name):
        """Set a specific theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.apply_theme()
            self.save_theme_preference()
    
    def apply_theme(self):
        """Apply the current theme to the application."""
        theme = self.themes[self.current_theme]
        
        # Configure root window
        self.root.configure(bg=theme['bg'])
        
        # Configure ttk style
        style = ttk.Style()
        
        # Configure various ttk widgets
        style.configure('TLabel', 
                       background=theme['bg'], 
                       foreground=theme['fg'])
        
        style.configure('TButton',
                       background=theme['button_bg'],
                       foreground=theme['button_fg'])
        
        style.configure('TEntry',
                       fieldbackground=theme['entry_bg'],
                       foreground=theme['entry_fg'],
                       bordercolor=theme['select_bg'])
        
        style.configure('TFrame',
                       background=theme['bg'])
        
        style.map('TButton',
                 background=[('active', theme['select_bg'])],
                 foreground=[('active', theme['select_fg'])])
        
        # Update existing widgets
        self.update_widget_colors(self.root, theme)
    
    def update_widget_colors(self, widget, theme):
        """Recursively update widget colors."""
        try:
            widget_class = widget.winfo_class()
            
            # Handle different widget types
            if widget_class == 'Text':
                widget.configure(bg=theme['entry_bg'], 
                               fg=theme['entry_fg'],
                               selectbackground=theme['select_bg'],
                               selectforeground=theme['select_fg'],
                               insertbackground=theme['fg'])
            
            elif widget_class == 'Listbox':
                widget.configure(bg=theme['entry_bg'],
                               fg=theme['entry_fg'],
                               selectbackground=theme['select_bg'],
                               selectforeground=theme['select_fg'])
            
            elif widget_class == 'Canvas':
                widget.configure(bg=theme['entry_bg'])
            
            elif widget_class in ['Frame', 'Toplevel']:
                widget.configure(bg=theme['bg'])
            
            # Recursively update children
            for child in widget.winfo_children():
                self.update_widget_colors(child, theme)
                
        except tk.TclError:
            # Some widgets might not support certain configurations
            pass
    
    def open_theme_selector(self):
        """Open theme selection window."""
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Theme Selector")
        theme_window.geometry("300x400")
        theme_window.configure(bg=self.themes[self.current_theme]['bg'])
        
        main_frame = ttk.Frame(theme_window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Select Theme:", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0, 20))
        
        # Theme selection buttons
        for i, (theme_name, theme_data) in enumerate(self.themes.items()):
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=i+1, column=0, pady=5, sticky=(tk.W, tk.E))
            
            # Theme preview
            preview_canvas = tk.Canvas(btn_frame, width=50, height=30,
                                     bg=theme_data['bg'], highlightthickness=1,
                                     highlightbackground=theme_data['fg'])
            preview_canvas.grid(row=0, column=0, padx=(0, 10))
            
            # Create preview elements
            preview_canvas.create_rectangle(5, 5, 20, 15, 
                                          fill=theme_data['button_bg'], 
                                          outline=theme_data['fg'])
            preview_canvas.create_text(30, 15, text="Aa", 
                                     fill=theme_data['fg'], 
                                     font=('Arial', 8))
            
            # Theme button
            theme_btn = ttk.Button(btn_frame, 
                                  text=f"{theme_name.title()} Theme",
                                  command=lambda t=theme_name: self.select_theme_and_close(t, theme_window))
            theme_btn.grid(row=0, column=1, sticky=(tk.W, tk.E))
            
            # Mark current theme
            if theme_name == self.current_theme:
                current_label = ttk.Label(btn_frame, text="(Current)", 
                                        font=('Arial', 8, 'italic'))
                current_label.grid(row=0, column=2, padx=(5, 0))
            
            btn_frame.columnconfigure(1, weight=1)
        
        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Theme Preview", padding="10")
        preview_frame.grid(row=len(self.themes)+2, column=0, pady=(20, 0), sticky=(tk.W, tk.E))
        
        ttk.Label(preview_frame, text="Sample Text").grid(row=0, column=0, sticky=tk.W)
        sample_entry = ttk.Entry(preview_frame, width=20)
        sample_entry.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        sample_entry.insert(0, "Sample input")
        
        ttk.Button(preview_frame, text="Sample Button").grid(row=2, column=0, pady=5)
        
        # Configure grid weights
        theme_window.columnconfigure(0, weight=1)
        theme_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
    
    def select_theme_and_close(self, theme_name, window):
        """Select theme and close the selector window."""
        self.set_theme(theme_name)
        window.destroy()
    
    def save_theme_preference(self):
        """Save current theme preference to file."""
        try:
            settings_file = os.path.join(self.data_dir, 'user_settings.json')
            
            settings = {}
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
            
            settings['theme'] = self.current_theme
            
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
        except Exception as e:
            print(f"Error saving theme preference: {e}")
    
    def load_theme_preference(self):
        """Load theme preference from file."""
        try:
            settings_file = os.path.join(self.data_dir, 'user_settings.json')
            
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
                    
                saved_theme = settings.get('theme', 'light')
                if saved_theme in self.themes:
                    self.current_theme = saved_theme
                    
        except Exception as e:
            print(f"Error loading theme preference: {e}")
    
    def get_current_theme_colors(self):
        """Get current theme color scheme."""
        return self.themes[self.current_theme]
