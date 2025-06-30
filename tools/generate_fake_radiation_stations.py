import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# Load municipalities polygons
nl = gpd.read_file('data/raw/municipalities.geojson')

np.random.seed(42)
n_stations = 30

# Randomly select 30 unique municipalities
selected = nl.sample(n=n_stations, random_state=42)
stations = []
for i, row in selected.iterrows():
    poly = row['geometry']
    # Generate a random point within the municipality polygon
    minx, miny, maxx, maxy = poly.bounds
    while True:
        lon = np.random.uniform(minx, maxx)
        lat = np.random.uniform(miny, maxy)
        pt = Point(lon, lat)
        if poly.contains(pt):
            break
    stations.append({
        'name': f'ST{str(len(stations)).zfill(2)}',
        'lat': lat,
        'lon': lon,
        'radiation': np.random.uniform(150, 900),
        'municipality': row['name'] if 'name' in row else row['Name']
    })
stations = pd.DataFrame(stations)
stations.to_csv('data/processed/radiation_stations.csv', index=False)
print('Fake station data (one per random municipality) written to data/processed/radiation_stations.csv')
