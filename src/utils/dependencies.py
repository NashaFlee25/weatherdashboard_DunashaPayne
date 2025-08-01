"""Dependency checker for optional packages."""

import tkinter as tk
from tkinter import messagebox


class DependencyChecker:
    """Handles checking and reporting of optional dependencies."""
    
    def __init__(self):
        """Initialize dependency checker."""
        self.has_matplotlib = self._check_matplotlib()
        self.has_pandas = self._check_pandas()
        self.has_requests = self._check_requests()
    
    def _check_matplotlib(self):
        """Check if matplotlib is available."""
        try:
            import matplotlib.pyplot as plt
            return True
        except ImportError:
            return False
    
    def _check_pandas(self):
        """Check if pandas is available."""
        try:
            import pandas as pd
            return True
        except ImportError:
            return False
    
    def _check_requests(self):
        """Check if requests is available."""
        try:
            import requests
            return True
        except ImportError:
            return False
    
    def show_warnings(self):
        """Show warnings for missing dependencies."""
        missing_deps = []
        
        if not self.has_requests:
            missing_deps.append("requests - Required for API calls")
        
        if not self.has_matplotlib:
            missing_deps.append("matplotlib - Optional for advanced visualizations")
        
        if not self.has_pandas:
            missing_deps.append("pandas - Optional for data analysis features")
        
        if missing_deps:
            warning_msg = "Missing optional dependencies:\n\n"
            warning_msg += "\n".join(f"• {dep}" for dep in missing_deps)
            warning_msg += "\n\nThe application will work with basic functionality."
            warning_msg += "\nTo install missing packages, run:"
            warning_msg += "\npip install " + " ".join(dep.split(" - ")[0] for dep in missing_deps)
            
            print("Dependency Warning:")
            print(warning_msg)
    
    def get_dependency_status(self):
        """Get status of all dependencies."""
        return {
            'matplotlib': self.has_matplotlib,
            'pandas': self.has_pandas,
            'requests': self.has_requests
        }
    
    def create_dependency_info_window(self, parent=None):
        """Create a window showing dependency information."""
        info_window = tk.Toplevel(parent) if parent else tk.Tk()
        info_window.title("Dependency Information")
        info_window.geometry("400x300")
        
        main_frame = tk.Frame(info_window, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="Dependency Status", 
                              font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        dependencies = [
            ('requests', self.has_requests, 'Required for weather API calls'),
            ('matplotlib', self.has_matplotlib, 'Optional for advanced charts'),
            ('pandas', self.has_pandas, 'Optional for data analysis')
        ]
        
        for name, available, description in dependencies:
            dep_frame = tk.Frame(main_frame)
            dep_frame.pack(fill=tk.X, pady=5)
            
            status_color = 'green' if available else 'red'
            status_text = '✓ Available' if available else '✗ Missing'
            
            tk.Label(dep_frame, text=f"{name}:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
            tk.Label(dep_frame, text=status_text, fg=status_color, 
                    font=('Arial', 10)).pack(side=tk.LEFT, padx=(10, 0))
            
            tk.Label(dep_frame, text=description, fg='gray', 
                    font=('Arial', 9)).pack(side=tk.LEFT, padx=(10, 0))
        
        # Installation instructions
        install_frame = tk.Frame(main_frame)
        install_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(install_frame, text="To install missing packages:", 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        missing_packages = [name for name, available, _ in dependencies if not available]
        if missing_packages:
            install_cmd = f"pip install {' '.join(missing_packages)}"
            tk.Label(install_frame, text=install_cmd, 
                    font=('Courier', 9), bg='lightgray').pack(fill=tk.X, pady=5)
        else:
            tk.Label(install_frame, text="All packages are installed!", 
                    fg='green').pack(anchor=tk.W)
        
        tk.Button(main_frame, text="Close", 
                 command=info_window.destroy).pack(pady=(20, 0))
