import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(layout="wide")
st.title("NL Radiation Interpolation Map (Kriging + IDW Blend)")

# Load NL boundary and station data
nl = gpd.read_file('data/raw/municipalities.geojson')
stations = pd.read_csv('data/processed/radiation_stations.csv')

# Load blended map
blended = pd.read_csv('data/processed/radiation_blended_map.csv', index_col=0)
lats = blended.index.astype(float)
lons = blended.columns.astype(float)
values = blended.values

# --- Main layout: Solar Density Map | Satellite ---
st.markdown("## Solar Density Map and Satellite (from main dashboard)")
st.markdown("(This section is a placeholder. See main dashboard for actual maps.)")
col1, col2 = st.columns(2)
with col1:
    st.info("Solar density map would be here.")
with col2:
    st.image(
        "https://modeles20.meteociel.fr/satellite/animsatvismtgde.gif",
        use_container_width=True
    )
    st.caption("Meteociel satellite image (auto-refreshes every 10 min)")

# --- Radiation Heatmap ---
st.markdown("---")
st.header("Interpolated Radiation Map (Kriging, IDW, or Blend)")

st.write("The colors represent the interpolated solar radiation intensity (W/m²):\n"
         "- Yellow = low\n- Orange = medium\n- Red = high\n\n"
         "The map is based on spatial interpolation of station data.")

# Map selection
map_options = {
    'Blended (Kriging+IDW, linear)': 'radiation_blended_map.csv',
    'IDW only': 'radiation_idw.csv',
    'Kriging (linear)': 'radiation_kriging_linear.csv',
    'Kriging (spherical)': 'radiation_kriging_spherical.csv',
    'Kriging (exponential)': 'radiation_kriging_exponential.csv',
    'Kriging (gaussian)': 'radiation_kriging_gaussian.csv',
}
map_choice = st.selectbox("Select map to display:", list(map_options.keys()), index=0)
map_path = f"data/processed/{map_options[map_choice]}"

# Load selected map
selected_map = pd.read_csv(map_path, index_col=0)
lats = selected_map.index.astype(float)
lons = selected_map.columns.astype(float)
values = selected_map.values

# Prepare grid for ImageOverlay (for smooth color fades)
from matplotlib import cm, colors
import matplotlib.pyplot as plt

min_val = np.nanmin(values)
max_val = np.nanmax(values)
if min_val == max_val:
    norm = np.ones_like(values) * 0.5
else:
    norm = (values - min_val) / (max_val - min_val)

cmap = cm.get_cmap('YlOrRd')
rgba_img = cmap(norm)
rgb_img = (rgba_img[:, :, :3] * 255).astype(np.uint8)

m = folium.Map(location=[52.2, 5.3], zoom_start=8)
folium.raster_layers.ImageOverlay(
    image=rgb_img,
    bounds=[[lats.min(), lons.min()], [lats.max(), lons.max()]],
    opacity=0.6,
    name='Radiation Heatmap',
    interactive=True,
    cross_origin=False,
    zindex=1,
).add_to(m)

# Color station markers by value
norm_station = (stations['radiation'] - min_val) / (max_val - min_val) if max_val > min_val else np.ones_like(stations['radiation']) * 0.5
for i, row in stations.iterrows():
    color = colors.rgb2hex(cmap(norm_station[i]))
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=1.0,
        popup=f"{row['name']}<br>Radiation: {row['radiation']:.1f}<br>{row['municipality']}"
    ).add_to(m)

# Add colorbar legend using matplotlib
import io
import base64
fig, ax = plt.subplots(figsize=(5, 0.5))
fig.subplots_adjust(bottom=0.5)
cbar = plt.colorbar(
    cm.ScalarMappable(norm=colors.Normalize(vmin=min_val, vmax=max_val), cmap=cmap),
    cax=ax, orientation='horizontal', label='Radiation (W/m²)')
buf = io.BytesIO()
plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
plt.close(fig)
buf.seek(0)
img_b64 = base64.b64encode(buf.read()).decode('utf-8')
st.markdown(f'<img src="data:image/png;base64,{img_b64}" style="display: block; margin-left: auto; margin-right: auto;"/>', unsafe_allow_html=True)

# Show the map and handle click query in one place
clicked = st_folium(m, width=900, height=600, returned_objects=["last_clicked"])

with st.expander("Query radiation at a point (click on map)"):
    st.write("Click on the map to see the interpolated radiation value at that location.")
    if clicked and clicked.get("last_clicked"):
        lat = clicked["last_clicked"]["lat"]
        lon = clicked["last_clicked"]["lng"]
        lat_idx = np.abs(lats - lat).argmin()
        lon_idx = np.abs(lons - lon).argmin()
        rad_val = values[lat_idx, lon_idx]
        st.success(f"Radiation at ({lat:.4f}, {lon:.4f}): {rad_val:.1f} W/m²")
