"""
Data package for weather dashboard.
"""
# This file makes the data directory a Python package
from .io import write_weather_record, read_weather_records, calculate_weather_statistics

__all__ = ['write_weather_record', 'read_weather_records', 'calculate_weather_statistics']
