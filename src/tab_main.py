import tkinter as tk
import os 
import sys
from tkinter import messagebox
from src.services.weather_service import WeatherService
import csv
from datetime import datetime
from src.services.gui_icons import GUIIcons
from src.services.ui_dashboard import WeatherDashboard


"""Tab Interface for Weather Dashboard Features
This module pulls all the tabs together from main to pull"""

Take those two tabs and put them together in a tab interface