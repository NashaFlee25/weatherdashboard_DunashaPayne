"""Dependency checking utilities."""

from tkinter import messagebox


class DependencyChecker:
    """Handles checking and reporting of optional dependencies."""
    
    def __init__(self):
        """Initialize dependency checker."""
        self.has_matplotlib = self._check_matplotlib()
        self.has_pandas = self._check_pandas()
    
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
    
    def show_warnings(self):
        """Show warnings for missing dependencies."""
        missing_deps = []
        if not self.has_matplotlib:
            missing_deps.append("matplotlib")
        if not self.has_pandas:
            missing_deps.append("pandas")
        
        if missing_deps:
            warning_msg = f"Missing dependencies: {', '.join(missing_deps)}\n"
            warning_msg += "Some features may be limited. Install with:\n"
            warning_msg += f"pip install {' '.join(missing_deps)}"
            
            messagebox.showwarning("Missing Dependencies", warning_msg)
