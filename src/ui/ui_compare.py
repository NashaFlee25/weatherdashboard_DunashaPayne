"""
Compare Cities page: team feature, data visualization.
"""
import customtkinter as ctk
import pandas as pd
from src.data_utils import load_team_data
import matplotlib.pyplot as plt
import seaborn as sns

class CompareCitiesPage(ctk.CTkFrame):
    def __init__(self, master, team_data_path, **kwargs):
        super().__init__(master, **kwargs)
        self.team_data_path = team_data_path
        self.data = load_team_data(team_data_path)
        self.compare_btn = ctk.CTkButton(self, text="Visualize Team Cities", command=self.visualize)
        self.compare_btn.pack(pady=10)
        self.result_label = ctk.CTkLabel(self, text="Team city data will appear here.")
        self.result_label.pack(pady=10)

    def visualize(self):
        if self.data.empty:
            self.result_label.configure(text="No team data found.")
            return
        plt.figure(figsize=(6, 4))
        sns.barplot(x="City", y="Temperature", data=self.data)
        plt.title("Team City Temperatures")
        plt.xlabel("City")
        plt.ylabel("Temperature (°C)")
        plt.tight_layout()
        plt.show()
        self.result_label.configure(text="Visualization shown.")
