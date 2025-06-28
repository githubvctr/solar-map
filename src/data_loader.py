import pandas as pd
import json
from pathlib import Path

def load_solar_data(csv_path="data/processed/2024_solar_data_and_coordinates_NL.csv") -> pd.DataFrame:
    """
    Loads the cleaned solar panel data from a CSV file.

    Args:
        csv_path (str): Path to the processed CSV file.

    Returns:
        pd.DataFrame: DataFrame containing solar panel data.
    """
    try:
        # Load CSV (assuming standard comma delimiter, update if needed)
        df = pd.read_csv(csv_path)

        # Print columns for debugging
        print("Dataset Loaded Successfully. Columns:", df.columns)

        return df
    except Exception as e:
        print(f"Error loading CSV file {csv_path}: {e}")
        return pd.DataFrame()

def csv_to_json(csv_file="data/processed/solar_data_and_coordinates_NL.csv", json_file="data/processed/solar_data.json"):
    """
    Converts the processed CSV file to JSON format.

    Args:
        csv_file (str): Path to the processed CSV file.
        json_file (str): Path to save the JSON file.
    """
    try:
        df = pd.read_csv(csv_file)
        df.to_json(json_file, orient="records", indent=4)
        print(f"Converted {csv_file} to {json_file}")
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")