"""
Feature: Tomorrow's Guess (simple prediction based on current data).
"""
import numpy as np

def guess_tomorrow_temperature(current_temp, history):
    # history: list of previous temperatures
    if history:
        avg_change = np.mean(np.diff(history))
        return current_temp + avg_change
    return current_temp
