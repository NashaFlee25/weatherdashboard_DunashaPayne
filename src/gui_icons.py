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
import ttkbootstrap as ttk_bs
from ttkbootstrap.constants import DANGER, DARK, INFO, LIGHT, PRIMARY, SECONDARY
from src.config.settings_manager import SettingsManager

class GUIIcons:   
    """weather condtion Icons using Unicode characters"""

    CLEAR = "clear_sky_icon
    PARTLY_CLOUDY = "few_clouds_icon"
    CLOUDY = "scattered_clouds_icon"
    OVERCAST = "overcast_clouds_icon"
    RAIN = "rain_icon"
    HEAVY_RAIN = "shower_rain_icon"
    SNOW = "snow_icon"
    FOG = "mist_icon"
    WIND = "wind_icon"
    HOT = "hot_icon"
    COLD = "cold_icon"
    DEFAULT = "default_icon"

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
        