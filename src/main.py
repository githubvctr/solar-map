from src.data_loader import load_solar_data, csv_to_json
from src.map_generator import create_solar_panel_map

if __name__ == "__main__":
    # Define file paths
    data_csv = "data/processed/solar_data_and_coordinates_NL.csv"
    geojson_file = "data/raw/municipalities.geojson"  # Updated path
    json_output = "data/processed/SP_data.json"
    output_map = "solar_map.html"

    # Convert CSV to JSON
    csv_to_json(data_csv, json_output)

    # Generate solar map
    create_solar_panel_map(data_csv, geojson_file, output_map)
