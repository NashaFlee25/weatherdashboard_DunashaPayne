"""Weather icons feature using canvas graphics."""

import tkinter as tk
from tkinter import ttk
import math


class WeatherIcons:
    """Feature for creating custom weather icons using canvas."""
    
    def __init__(self):
        """Initialize weather icons feature."""
        self.icon_size = 100
        self.icon_mappings = {
            'clear': self.draw_sun,
            'sunny': self.draw_sun,
            'sun': self.draw_sun,
            'cloud': self.draw_cloud,
            'clouds': self.draw_cloud,
            'cloudy': self.draw_cloud,
            'overcast': self.draw_overcast,
            'rain': self.draw_rain,
            'rainy': self.draw_rain,
            'drizzle': self.draw_drizzle,
            'snow': self.draw_snow,
            'snowy': self.draw_snow,
            'storm': self.draw_storm,
            'thunderstorm': self.draw_storm,
            'fog': self.draw_fog,
            'mist': self.draw_fog,
            'wind': self.draw_wind,
            'windy': self.draw_wind
        }
    
    def create_weather_icon(self, parent, weather_description, size=100):
        """Create a weather icon canvas based on description."""
        self.icon_size = size
        canvas = tk.Canvas(parent, width=size, height=size, bg='lightblue')
        
        # Find appropriate icon based on description
        icon_func = self.get_icon_function(weather_description.lower())
        icon_func(canvas)
        
        return canvas
    
    def get_icon_function(self, description):
        """Get the appropriate icon drawing function."""
        for keyword in self.icon_mappings:
            if keyword in description:
                return self.icon_mappings[keyword]
        
        # Default to cloud if no match found
        return self.draw_cloud
    
    def draw_sun(self, canvas):
        """Draw a sun icon."""
        center = self.icon_size // 2
        sun_radius = self.icon_size // 4
        
        # Draw sun rays
        for i in range(8):
            angle = i * math.pi / 4
            start_x = center + sun_radius * 1.3 * math.cos(angle)
            start_y = center + sun_radius * 1.3 * math.sin(angle)
            end_x = center + sun_radius * 1.7 * math.cos(angle)
            end_y = center + sun_radius * 1.7 * math.sin(angle)
            
            canvas.create_line(start_x, start_y, end_x, end_y, 
                             fill='orange', width=3, capstyle='round')
        
        # Draw sun circle
        canvas.create_oval(center - sun_radius, center - sun_radius,
                          center + sun_radius, center + sun_radius,
                          fill='yellow', outline='orange', width=2)
        
        # Draw sun face
        eye_offset = sun_radius // 3
        canvas.create_oval(center - eye_offset - 3, center - eye_offset - 3,
                          center - eye_offset + 3, center - eye_offset + 3,
                          fill='orange')
        canvas.create_oval(center + eye_offset - 3, center - eye_offset - 3,
                          center + eye_offset + 3, center - eye_offset + 3,
                          fill='orange')
        
        # Smile
        canvas.create_arc(center - eye_offset, center - 5,
                         center + eye_offset, center + eye_offset,
                         start=0, extent=180, style='arc', outline='orange', width=2)
    
    def draw_cloud(self, canvas):
        """Draw a cloud icon."""
        center = self.icon_size // 2
        cloud_width = self.icon_size // 1.5
        cloud_height = self.icon_size // 2.5
        
        # Draw cloud base
        canvas.create_oval(center - cloud_width//2, center - cloud_height//2,
                          center + cloud_width//2, center + cloud_height//2,
                          fill='white', outline='gray', width=2)
        
        # Draw cloud bumps
        bump_radius = cloud_height // 3
        for i in range(3):
            x_offset = (i - 1) * cloud_width // 3
            canvas.create_oval(center + x_offset - bump_radius, center - cloud_height//2 - bump_radius//2,
                              center + x_offset + bump_radius, center - cloud_height//2 + bump_radius//2,
                              fill='white', outline='gray', width=2)
    
    def draw_overcast(self, canvas):
        """Draw overcast clouds."""
        center = self.icon_size // 2
        
        # Draw multiple overlapping gray clouds
        for i in range(3):
            x_offset = (i - 1) * 15
            y_offset = (i - 1) * 10
            
            canvas.create_oval(center + x_offset - 25, center + y_offset - 15,
                              center + x_offset + 25, center + y_offset + 15,
                              fill='lightgray', outline='gray', width=1)
    
    def draw_rain(self, canvas):
        """Draw rain icon (cloud with rain drops)."""
        # Draw cloud first
        self.draw_cloud(canvas)
        
        center = self.icon_size // 2
        
        # Draw rain drops
        for i in range(5):
            x = center - 30 + i * 15
            y_start = center + 15
            y_end = center + 35
            
            canvas.create_line(x, y_start, x, y_end, 
                             fill='blue', width=2, capstyle='round')
            canvas.create_oval(x - 2, y_end - 2, x + 2, y_end + 2, 
                              fill='blue', outline='blue')
    
    def draw_drizzle(self, canvas):
        """Draw drizzle icon (light rain)."""
        # Draw cloud first
        self.draw_cloud(canvas)
        
        center = self.icon_size // 2
        
        # Draw light rain drops
        for i in range(3):
            x = center - 20 + i * 20
            y_start = center + 15
            y_end = center + 30
            
            canvas.create_line(x, y_start, x, y_end, 
                             fill='lightblue', width=1, capstyle='round')
    
    def draw_snow(self, canvas):
        """Draw snow icon (cloud with snowflakes)."""
        # Draw cloud first
        self.draw_cloud(canvas)
        
        center = self.icon_size // 2
        
        # Draw snowflakes
        for i in range(4):
            x = center - 25 + i * 17
            y = center + 20 + (i % 2) * 10
            
            # Draw snowflake
            canvas.create_line(x - 4, y, x + 4, y, fill='white', width=2)
            canvas.create_line(x, y - 4, x, y + 4, fill='white', width=2)
            canvas.create_line(x - 3, y - 3, x + 3, y + 3, fill='white', width=1)
            canvas.create_line(x - 3, y + 3, x + 3, y - 3, fill='white', width=1)
    
    def draw_storm(self, canvas):
        """Draw storm icon (dark cloud with lightning)."""
        center = self.icon_size // 2
        
        # Draw dark cloud
        canvas.create_oval(center - 30, center - 20, center + 30, center + 20,
                          fill='darkgray', outline='black', width=2)
        
        # Draw lightning bolt
        lightning_points = [
            center - 5, center + 10,
            center + 5, center + 25,
            center, center + 25,
            center + 10, center + 40,
            center + 5, center + 30,
            center - 5, center + 30
        ]
        canvas.create_polygon(lightning_points, fill='yellow', outline='orange', width=1)
    
    def draw_fog(self, canvas):
        """Draw fog icon (horizontal wavy lines)."""
        center = self.icon_size // 2
        
        # Draw fog lines
        for i in range(4):
            y = center - 20 + i * 15
            
            # Create wavy line using multiple small lines
            points = []
            for x in range(0, self.icon_size, 5):
                wave_y = y + 3 * math.sin(x * 0.1)
                points.extend([x, wave_y])
            
            if len(points) >= 4:
                canvas.create_line(points, fill='lightgray', width=3, smooth=True)
    
    def draw_wind(self, canvas):
        """Draw wind icon (curved lines)."""
        center = self.icon_size // 2
        
        # Draw wind lines
        for i in range(3):
            y = center - 15 + i * 15
            
            # Create curved wind line
            canvas.create_arc(center - 30, y - 5, center + 10, y + 5,
                             start=0, extent=180, style='arc', 
                             outline='gray', width=3)
            
            canvas.create_arc(center - 10, y - 5, center + 30, y + 5,
                             start=180, extent=180, style='arc', 
                             outline='gray', width=2)
    
    def create_icon_demo_window(self):
        """Create a demo window showing all weather icons."""
        demo_window = tk.Toplevel()
        demo_window.title("Weather Icons Demo")
        demo_window.geometry("600x400")
        
        main_frame = ttk.Frame(demo_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(main_frame, text="Weather Icons Demo", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # Create demo icons
        icons = [
            ('Sunny', 'clear sky'),
            ('Cloudy', 'scattered clouds'),
            ('Rainy', 'light rain'),
            ('Snowy', 'light snow'),
            ('Stormy', 'thunderstorm'),
            ('Foggy', 'fog'),
            ('Windy', 'strong wind'),
            ('Overcast', 'overcast clouds')
        ]
        
        for i, (name, description) in enumerate(icons):
            row = 1 + i // 4
            col = i % 4
            
            frame = ttk.Frame(main_frame)
            frame.grid(row=row, column=col, padx=10, pady=10)
            
            ttk.Label(frame, text=name, font=('Arial', 10, 'bold')).pack()
            icon_canvas = self.create_weather_icon(frame, description, 80)
            icon_canvas.pack(pady=5)
