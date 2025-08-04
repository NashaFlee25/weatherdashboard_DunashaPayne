"""
Feature: Temperature Graph using matplotlib/seaborn.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_temperature_graph(weather_data, city):
    # weather_data: list of dicts with 'temperature' and 'date'
    df = pd.DataFrame(weather_data)
    plt.figure(figsize=(6, 4))
    sns.lineplot(x="date", y="temperature", data=df, marker="o")
    plt.title(f"Temperature Trend for {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.tight_layout()
    plt.show()
