## File: test_knmi_loader.py

## File: tests/__init__.py

## File: streamlit_app/app.py
- def load_and_prepare_data():

## File: streamlit_app/ui/sidebar.py
- def capacity_filter_slider(max_capacity, default):
- def enable_selection_mode():
- def display_selection_summary(gdf):

## File: streamlit_app/ui/legend.py
- def create_colormap(gdf):
- def create_custom_legend(colormap):

## File: streamlit_app/ui/map.py
- def build_map(gdf, colormap, filtered, enable_selection):

## File: src/knmi_loader.py
- def list_available_files():
- def get_file_url(filename):
- def download_latest_dataframe():

## File: src/data_loader.py
- def load_solar_data(csv_path):
    """Loads the cleaned solar panel data from a CSV file."""
- def csv_to_json(csv_file, json_file):
    """Converts the processed CSV file to JSON format."""

## File: src/__init__.py

## File: src/utils.py

## File: src/map_generator.py
- def create_solar_panel_map(data_file, geojson_file, output_file):
    """Generates an interactive solar panel capacity map with a color gradient,"""

## File: src/main.py

## File: src/temp_module.py
- def my_func(a):
