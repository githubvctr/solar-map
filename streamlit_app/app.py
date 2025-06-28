import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

import streamlit as st
from streamlit_folium import st_folium
from folium import Map
import ast
from shapely.geometry import Polygon, Point
import geopandas as gpd
import branca.colormap as cm
from data_loader import load_solar_data

from ui.sidebar import (
    capacity_filter_slider,
    enable_selection_mode,
    display_selection_summary,
)
from ui.map import build_map
from ui.legend import create_custom_legend

# --- Initialize session state for selection ---
if "selected_municipalities" not in st.session_state:
    st.session_state.selected_municipalities = []

@st.cache_data
def load_and_prepare_data():
    df = load_solar_data()
    # Only keep Name, Coordinates, and Installaties (aantal)
    df = df[["Name", "Coordinates", "Installaties (aantal)"]]
    # Remove rows with NaN in key columns
    df = df.dropna(subset=["Name", "Coordinates", "Installaties (aantal)"])
    df["Coordinates"] = df["Coordinates"].apply(ast.literal_eval)
    def safe_polygon(coords):
        if not coords:
            return None
        # Handle MultiPolygon (list of polygons)
        if isinstance(coords[0][0][0], (float, int)):
            # MultiPolygon: take first polygon
            shell = coords[0]
        elif isinstance(coords[0][0], (float, int)):
            # Polygon: take as is
            shell = coords
        else:
            return None
        if len(shell) < 3:
            return None
        try:
            return Polygon(shell)
        except Exception:
            return None
    df["geometry"] = df["Coordinates"].apply(safe_polygon)
    df = df[df["geometry"].notnull()]
    return gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:4326")

# --- UI Layout ---
st.set_page_config(layout="wide")
st.title("NL Solar PV Capacity Map")

# --- Load Data ---
gdf = load_and_prepare_data()
min_installations = capacity_filter_slider(gdf["Installaties (aantal)"].max())
filtered = gdf[gdf["Installaties (aantal)"] >= min_installations]

# --- Colormap ---
colormap = cm.linear.YlOrRd_09.scale(
    gdf["Installaties (aantal)"].min(), gdf["Installaties (aantal)"].max()
)
colormap.caption = "Number of Installations"

# --- Enable interactive selection ---
enable_selection = enable_selection_mode()

# --- Build Map ---
m = build_map(gdf, colormap, filtered, enable_selection)

# # --- Add Custom Legend ---
# legend = create_custom_legend(colormap)
# m.add_child(legend)

# --- Display Map ---
output = st_folium(m, width=1100, height=700)

# --- Handle Selections ---
if enable_selection:
    clicked = output.get("last_clicked")
    if clicked:
        pt = Point(clicked["lng"], clicked["lat"])
        match = gdf[gdf.geometry.contains(pt)]

        if not match.empty:
            name = match.iloc[0]["Name"]
            if name in st.session_state.selected_municipalities:
                st.session_state.selected_municipalities.remove(name)
            else:
                st.session_state.selected_municipalities.append(name)

# --- Sidebar Summary ---
display_selection_summary(gdf)
