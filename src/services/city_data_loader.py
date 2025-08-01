"""City data loading service for extracting city names from CSV files."""

import pandas as pd
import os
from typing import List, Optional


class CityDataLoader:
    """Service class for loading and managing city data from CSV files."""
    
    def __init__(self, csv_file_path: str):
        """
        Initialize the city data loader.
        
        Args:
            csv_file_path (str): Path to the CSV file containing city data
        """
        self.csv_file_path = csv_file_path
        self._city_names: List[str] = []
        self._load_cities()
    
    def _load_cities(self) -> None:
        """Load city names from the CSV file."""
        try:
            if not os.path.exists(self.csv_file_path):
                print(f"Warning: CSV file {self.csv_file_path} not found.")
                self._city_names = []
                return
            
            df = pd.read_csv(self.csv_file_path)
            
            # Try different possible column names for cities
            city_column = self._find_city_column(df)
            
            if city_column:
                self._city_names = sorted(
                    df[city_column].dropna().unique().tolist()
                )
                print(f"Loaded {len(self._city_names)} unique cities from {self.csv_file_path}")
            else:
                print("Warning: No city column found in CSV file.")
                self._city_names = []
                
        except Exception as e:
            print(f"Error loading cities from CSV: {e}")
            self._city_names = []
    
    def _find_city_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Find the column containing city names.
        
        Args:
            df (pd.DataFrame): DataFrame to search for city column
            
        Returns:
            Optional[str]: Name of the city column if found, None otherwise
        """
        possible_city_columns = ['City', 'city', 'CITY', 'City Name', 'city_name']
        
        for col in possible_city_columns:
            if col in df.columns:
                return col
        
        # If no standard column name found, use the first column
        if len(df.columns) > 0:
            return df.columns[0]
        
        return None
    
    def get_city_names(self) -> List[str]:
        """
        Get the list of unique city names.
        
        Returns:
            List[str]: Sorted list of unique city names
        """
        return self._city_names.copy()
    
    def refresh_cities(self) -> None:
        """Refresh the city list by reloading from the CSV file."""
        print("Refreshing city data from CSV...")
        self._load_cities()
    
    def is_valid_city(self, city_name: str) -> bool:
        """
        Check if a city name exists in the loaded data.
        
        Args:
            city_name (str): Name of the city to check
            
        Returns:
            bool: True if city exists, False otherwise
        """
        return city_name in self._city_names
    
    def get_city_count(self) -> int:
        """
        Get the number of unique cities loaded.
        
        Returns:
            int: Number of unique cities
        """
        return len(self._city_names)
