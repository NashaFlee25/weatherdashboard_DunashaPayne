"""
Simple weather prediction feature.
"""
import numpy as np
from typing import List, Optional

def predict_tomorrow_temperature(current_temp: float, history: List[float]) -> float:
    """
    Predict tomorrow's temperature based on current temperature and historical data.
    
    Args:
        current_temp: Current temperature
        history: List of previous temperatures
        
    Returns:
        Predicted temperature for tomorrow
    """
    if not history or len(history) < 2:
        return current_temp
    
    # Calculate average daily change
    changes = np.diff(history[-7:]) if len(history) >= 7 else np.diff(history)
    avg_change = np.mean(changes)
    
    # Apply seasonal adjustment (simple)
    predicted_temp = current_temp + avg_change
    
    return round(predicted_temp, 1)
