from solar_map.data_loader import load_solar_data, csv_to_json
from solar_map.map_generator import create_solar_panel_map
import webbrowser
import os

if __name__ == "__main__":
    # Define file paths
    data_csv = "data/processed/solar_data_and_coordinates_NL.csv"
    geojson_file = "data/raw/municipalities.geojson"
    json_output = "data/processed/SP_data.json"
    output_map = "solar_map.html"

    # Convert CSV to JSON
    csv_to_json(data_csv, json_output)

    # Generate solar map
    create_solar_panel_map(data_csv, geojson_file, output_map)

    # Open in default browser
    # If the file path is relative, turn it into an absolute file:// URL:
    file_url = f"file://{os.path.abspath(output_map)}"
    webbrowser.open_new_tab(file_url)
