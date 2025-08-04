"""
Utility functions for loading/saving CSV/JSON data.
"""
import pandas as pd
import json

def load_team_data(csv_path):
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error loading team data: {e}")
        return pd.DataFrame()

def export_to_csv(data, filename):
    try:
        data.to_csv(filename, index=False)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False

def export_to_json(data, filename):
    try:
        data.to_json(filename, orient="records")
        return True
    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False
