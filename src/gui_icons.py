import os
from typing import Optional, Dict, Any, Callable, List
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random 
import json
import logging
import random
import threading
import tkinter.font as tkFont
from datetime import date, datetime
from src.config.settings_manager import SettingsManager

class GUIIcons:
    """Weather condition icons using Unicode characters"""

    CLEAR = "☀️"              # Clear sky
    PARTLY_CLOUDY = "🌤️"      # Few clouds
    CLOUDY = "⛅"              # Scattered clouds
    OVERCAST = "☁️"           # Overcast clouds
    RAIN = "🌧️"               # Rain
    HEAVY_RAIN = "🌦️"         # Shower rain
    SNOW = "❄️"               # Snow
    FOG = "🌫️"                # Mist / Fog
    WIND = "💨"               # Wind
    HOT = "🔥"                # Hot
    COLD = "🧊"               # Cold
    DEFAULT = "❔"            # Default / Unknown
    THUNDERSTORM = "⛈️"      # Thunderstorm
    
    @classmethod
    def get_icon(cls, condition: str, temperture: Optional[float] = None) -> str:
        condition = condition.lower()

        # Temperture Icons
        if temperture is not None:
            if temperture > 30:
                return cls.HOT
            elif temperture < 0:
                return cls.COLD
            
            # Condition based Icons
        if "clear" in condition.lower or "sunny" in condition.lower:
            return cls.CLEAR
        elif "cloud" in condition.lower or "cloudy" in condition.lower:
            return cls.CLOUDY
        elif "partly" in condition.lower or "scattered" in condition.lower:
            return cls.PARTLY_CLOUDY
        elif "overcast" in condition.lower:
            return cls.OVERCAST
        elif "rain" in condition.lower or "shower" in condition.lower:
            return cls.RAIN
        elif "heavy" in condition.lower or "storm" in condition.lower:
            return cls.HEAVY_RAIN
        elif "thunder" in condition.lower or "lightning" in condition.lower:
            return cls.THUNDERSTORM
        elif "snow" in condition.lower or "blizzard" in condition.lower:
            return cls.SNOW
        elif "mist" in condition.lower or "fog" in condition.lower:
            return cls.FOG
        elif "wind" in condition.lower:
            return cls.WIND
        else:
            return cls.DEFAULT
        