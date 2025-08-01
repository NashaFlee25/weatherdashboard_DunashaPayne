"""Chart and visualization management for the Weather Dashboard."""

import tkinter as tk
from tkinter import ttk

try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


class ChartManager:
    """Manages chart creation and data visualization."""
    
    def __init__(self):
        """Initialize the chart manager."""
        self.has_matplotlib = HAS_MATPLOTLIB
    
    def create_comparison_display(self, parent_frame, city1_data, city2_data, selected_cities):
        """Create comparison visualization based on available libraries."""
        if self.has_matplotlib:
            self._create_comparison_chart(parent_frame, city1_data, city2_data, selected_cities)
        else:
            self._create_comparison_table(parent_frame, city1_data, city2_data, selected_cities)
    
    def _create_comparison_chart(self, parent_frame, city1_data, city2_data, selected_cities):
        """Create weather comparison charts using matplotlib."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"Weather Comparison: {selected_cities['city1']} vs {selected_cities['city2']}", 
                     fontsize=16, fontweight='bold')
        
        # Temperature comparison
        self._plot_metric_comparison(ax1, city1_data, city2_data, selected_cities, 
                                   'temperature', 'Temperature Trends', 'Temperature (°F)')
        
        # Humidity comparison
        self._plot_metric_comparison(ax2, city1_data, city2_data, selected_cities,
                                   'humidity', 'Humidity Levels', 'Humidity (%)')
        
        # Precipitation comparison
        self._plot_precipitation_comparison(ax3, city1_data, city2_data, selected_cities)
        
        # Wind speed comparison
        self._plot_windspeed_comparison(ax4, city1_data, city2_data, selected_cities)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def _plot_metric_comparison(self, ax, city1_data, city2_data, selected_cities, metric, title, ylabel):
        """Plot comparison for a specific metric."""
        if metric in city1_data.columns and metric in city2_data.columns:
            ax.plot(city1_data.index, city1_data[metric], label=selected_cities['city1'], color='blue')
            ax.plot(city2_data.index, city2_data[metric], label=selected_cities['city2'], color='red')
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.legend()
            ax.grid(True)
    
    def _plot_precipitation_comparison(self, ax, city1_data, city2_data, selected_cities):
        """Plot precipitation comparison."""
        if 'precipitation' in city1_data.columns and 'precipitation' in city2_data.columns:
            ax.bar([selected_cities['city1']], [city1_data['precipitation'].mean()], 
                   color='blue', alpha=0.7)
            ax.bar([selected_cities['city2']], [city2_data['precipitation'].mean()], 
                   color='red', alpha=0.7)
            ax.set_title('Average Precipitation')
            ax.set_ylabel('Precipitation (inches)')
    
    def _plot_windspeed_comparison(self, ax, city1_data, city2_data, selected_cities):
        """Plot wind speed comparison."""
        if 'wind_speed' in city1_data.columns and 'wind_speed' in city2_data.columns:
            ax.boxplot([city1_data['wind_speed'].dropna(), city2_data['wind_speed'].dropna()],
                      labels=[selected_cities['city1'], selected_cities['city2']])
            ax.set_title('Wind Speed Distribution')
            ax.set_ylabel('Wind Speed (mph)')
    
    def _create_comparison_table(self, parent_frame, city1_data, city2_data, selected_cities):
        """Create weather comparison table (fallback for no matplotlib)."""
        comparison_frame = ttk.LabelFrame(parent_frame, text="Weather Comparison")
        comparison_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ('Metric', selected_cities['city1'], selected_cities['city2'])
        tree = ttk.Treeview(comparison_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(comparison_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Calculate metrics
        metrics = self._calculate_comparison_metrics(city1_data, city2_data)
        
        for metric in metrics:
            tree.insert('', 'end', values=metric)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _calculate_comparison_metrics(self, city1_data, city2_data):
        """Calculate comparison metrics for table display."""
        metrics = []
        if hasattr(city1_data, 'columns'):
            for col in city1_data.columns:
                if col in city2_data.columns and city1_data[col].dtype in ['float64', 'int64']:
                    city1_avg = city1_data[col].mean()
                    city2_avg = city2_data[col].mean()
                    metrics.append((col.title(), f"{city1_avg:.2f}", f"{city2_avg:.2f}"))
        else:
            for key in city1_data:
                if key in city2_data and isinstance(city1_data[key], (int, float)):
                    metrics.append((key.title(), f"{city1_data[key]:.2f}", f"{city2_data[key]:.2f}"))
        return metrics
    
    def display_city_stats(self, parent, city_name, city_data):
        """Display statistics for a single city."""
        city_frame = ttk.LabelFrame(parent, text=f"{city_name} Statistics")
        city_frame.pack(fill="x", padx=5, pady=5)
        
        stats_text = tk.Text(city_frame, height=10, width=50)
        stats_text.pack(side="left", padx=10, pady=10)
        
        stats_content = self._generate_stats_content(city_name, city_data)
        stats_text.insert("1.0", stats_content)
        stats_text.config(state="disabled")
    
    def _generate_stats_content(self, city_name, city_data):
        """Generate statistics content for display."""
        stats_content = f"City: {city_name}\n"
        
        if hasattr(city_data, 'columns'):
            stats_content += f"Data Points: {len(city_data)}\n\n"
            for column in city_data.select_dtypes(include=['float64', 'int64']).columns:
                stats_content += f"{column.title()}:\n"
                stats_content += f"  Mean: {city_data[column].mean():.2f}\n"
                stats_content += f"  Min: {city_data[column].min():.2f}\n"
                stats_content += f"  Max: {city_data[column].max():.2f}\n"
                stats_content += f"  Std Dev: {city_data[column].std():.2f}\n\n"
        else:
            stats_content += f"Data Type: Single record\n\n"
            for key, value in city_data.items():
                if isinstance(value, (int, float)):
                    stats_content += f"{key.title()}: {value:.2f}\n"
                else:
                    stats_content += f"{key.title()}: {value}\n"
        
        return stats_content
    
    def create_trends_chart(self, parent_frame, selected_cities, city_loader):
        """Create weather trends chart."""
        if not self.has_matplotlib:
            return
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        fig.suptitle("Weather Trends Over Time", fontsize=16, fontweight='bold')
        
        colors = ['blue', 'red', 'green', 'orange']
        
        self._plot_trends_for_metric(axes[0], selected_cities, city_loader, 
                                   'temperature', 'Temperature Trends', 'Temperature (°F)', colors)
        
        self._plot_trends_for_metric(axes[1], selected_cities, city_loader,
                                   'humidity', 'Humidity Trends', 'Humidity (%)', colors)
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def _plot_trends_for_metric(self, ax, selected_cities, city_loader, metric, title, ylabel, colors):
        """Plot trends for a specific metric."""
        color_index = 0
        for city_key, city_name in selected_cities.items():
            if city_name:
                city_data = city_loader.get_weather_data(city_name)
                if (city_data is not None and hasattr(city_data, 'columns') 
                    and metric in city_data.columns):
                    ax.plot(city_data.index, city_data[metric], 
                           label=city_name, color=colors[color_index % len(colors)])
                    color_index += 1
        
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True)
    
    def display_current_weather(self, parent, city_name, city_data):
        """Display current weather for a city."""
        if hasattr(city_data, 'iloc') and not city_data.empty:
            latest_data = city_data.iloc[-1]
        elif isinstance(city_data, dict):
            latest_data = city_data
        else:
            return
        
        city_frame = ttk.LabelFrame(parent, text=f"Current Weather - {city_name}")
        city_frame.pack(fill="x", padx=5, pady=5)
        
        weather_fields = ['temperature', 'humidity', 'wind_speed', 'precipitation']
        units = {'temperature': '°F', 'humidity': '%', 'wind_speed': ' mph', 'precipitation': ' inches'}
        
        row = 0
        for field in weather_fields:
            if field in latest_data:
                ttk.Label(city_frame, text=f"{field.title()}:").grid(row=row, column=0, sticky="w", padx=5, pady=2)
                value = latest_data[field]
                unit = units.get(field, '')
                display_value = f"{value:.1f}{unit}" if isinstance(value, (int, float)) else str(value)
                ttk.Label(city_frame, text=display_value).grid(row=row, column=1, sticky="w", padx=5, pady=2)
                row += 1
