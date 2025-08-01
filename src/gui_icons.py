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
    def get_icon(cls, condition: str, temperature: Optional[float] = None) -> str:
        condition = condition.lower()

        # Temperature Icons
        if temperature is not None:
            if temperature > 30:
                return cls.HOT
            elif temperature < 0:
                return cls.COLD
            
        # Condition based Icons
        if "clear" in condition or "sunny" in condition:
            return cls.CLEAR
        elif "few" in condition or "partly" in condition:
            return cls.PARTLY_CLOUDY
        elif "scattered" in condition or "broken" in condition:
            return cls.CLOUDY
        elif "overcast" in condition:
            return cls.OVERCAST
        elif "rain" in condition or "shower" in condition:
            return cls.RAIN
        elif "heavy" in condition or "storm" in condition:
            return cls.HEAVY_RAIN
        elif "thunder" in condition or "lightning" in condition:
            return cls.THUNDERSTORM
        elif "snow" in condition or "blizzard" in condition:
            return cls.SNOW
        elif "mist" in condition or "fog" in condition:
            return cls.FOG
        elif "wind" in condition:
            return cls.WIND
        else:
            return cls.DEFAULT
