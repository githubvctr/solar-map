import folium
import pandas as pd
import json
import numpy as np
import branca

def create_solar_panel_map(data_file="data/processed/solar_data_and_coordinates_NL.csv", 
                           geojson_file="data/raw/municipalities.geojson", 
                           output_file="solar_map.html"):
    """
    Generates an interactive solar panel capacity map with a color gradient,
    displaying both municipality name and installed capacity in the tooltip.

    Args:
        data_file (str): Path to the processed CSV file containing solar panel data.
        geojson_file (str): Path to the GeoJSON file containing municipality boundaries.
        output_file (str, optional): Path to save the output HTML file.
    """
    try:
        # Load solar panel data
        df = pd.read_csv(data_file)

        # Rename columns to match expected names
        df.rename(columns={
            "Name": "Region", 
            "Opgesteld vermogen van zonnepanelen (kW)": "Capacity_kW"
        }, inplace=True)

        # Build a dictionary mapping region to installed capacity
        capacity_dict = dict(zip(df["Region"], df["Capacity_kW"]))

        # Load GeoJSON data
        with open(geojson_file, "r") as f:
            geo_data = json.load(f)

        # Inject capacity data into each feature's properties so we can show it in the tooltip
        for feature in geo_data["features"]:
            mun_name = feature["properties"].get("name", "")
            # If there's a matching municipality in capacity_dict, add capacity to the GeoJSON
            feature["properties"]["Capacity_kW"] = capacity_dict.get(mun_name, 0)

        # Determine min/max capacity for color scaling
        min_capacity = df["Capacity_kW"].min()
        max_capacity = df["Capacity_kW"].max()

        # Define color gradient levels using percentiles
        bins = np.percentile(df["Capacity_kW"], [10, 20, 40, 60, 80, 90])
        colors = ['#ffffcc', '#ffeda0', '#feb24c', '#fd8d3c', '#e31a1c', '#b10026']

        def get_color(capacity):
            """Assigns a color based on capacity levels."""
            for i, threshold in enumerate(bins):
                if capacity <= threshold:
                    return colors[i]
            return colors[-1]

        # Create the map centered in the Netherlands
        solar_map = folium.Map(location=[52.1326, 5.2913], zoom_start=8)

        # Add GeoJSON layer with styling
        folium.GeoJson(
            geo_data,
            name="Solar Panel Capacity",
            style_function=lambda feature: {
                "fillColor": get_color(feature["properties"]["Capacity_kW"]),
                "fillOpacity": 0.7,
                "color": "gray",
                "weight": 0.5,
            },
            highlight_function=lambda feature: {"fillColor": "#ffffb2"},
            # Show both municipality name and capacity in the tooltip
            tooltip=folium.GeoJsonTooltip(
                fields=["name", "Capacity_kW"],
                aliases=["Municipality:", "Installed Capacity (kW):"],
                labels=True,
                sticky=True,
                localize=True
            )
        ).add_to(solar_map)

        # Add a color legend
        colormap = branca.colormap.LinearColormap(
            colors=colors,
            vmin=min_capacity,
            vmax=max_capacity,
            caption="Installed Solar Capacity (kW)"
        )
        colormap.add_to(solar_map)

        # Save the generated map
        solar_map.save(output_file)
        print(f"Map successfully saved as {output_file}")

    except Exception as e:
        print(f"Error generating map: {e}")
