import numpy as np
import pandas as pd
from pykrige.ok import OrdinaryKriging
from scipy.spatial import distance_matrix
import numpy.ma as ma

# Example: Load your station data (replace with your real data path)
stations = pd.read_csv('data/processed/radiation_stations.csv')  # columns: name, lat, lon, radiation

# Define grid over NL (adjust bounds as needed)
lats = np.linspace(50.7, 53.6, 100)
lons = np.linspace(3.3, 7.2, 100)
grid_lon, grid_lat = np.meshgrid(lons, lats)

# Try different variogram models and save all maps for comparison
kriging_maps = {}
kriging_vars = {}
for model in ['linear', 'spherical', 'exponential', 'gaussian']:
    OK = OrdinaryKriging(
        stations['lon'], stations['lat'], stations['radiation'],
        variogram_model=model, verbose=False, enable_plotting=False
    )
    k_map, k_var = OK.execute('grid', lons, lats)
    if ma.isMaskedArray(k_map):
        k_map = k_map.filled(np.nan)
    if ma.isMaskedArray(k_var):
        k_var = k_var.filled(np.nan)
    kriging_maps[model] = k_map
    kriging_vars[model] = k_var
    pd.DataFrame(k_map, index=lats, columns=lons).to_csv(f'data/processed/radiation_kriging_{model}.csv')
    pd.DataFrame(k_var, index=lats, columns=lons).to_csv(f'data/processed/radiation_krigingvar_{model}.csv')

# IDW interpolation (same as before)
def idw(xy, values, xi, power=2):
    dists = distance_matrix(xi, xy)
    dists[dists == 0] = 1e-10
    weights = 1 / dists**power
    weights /= weights.sum(axis=1)[:, None]
    return np.dot(weights, values)

xy = stations[['lon', 'lat']].values
values = stations['radiation'].values
xi = np.column_stack([grid_lon.ravel(), grid_lat.ravel()])
idw_map = idw(xy, values, xi).reshape(grid_lon.shape)
pd.DataFrame(idw_map, index=lats, columns=lons).to_csv('data/processed/radiation_idw.csv')

# Blend using the 'linear' model for now (can be changed)
kriging_map = kriging_maps['linear']
kriging_var = kriging_vars['linear']
var_min = np.nanmin(kriging_var)
var_max = np.nanmax(kriging_var)
if var_max == var_min:
    norm_var = np.ones_like(kriging_var) * 0.5
else:
    norm_var = (kriging_var - var_min) / (var_max - var_min)
alpha = 1 - norm_var
final_map = alpha * kriging_map + (1 - alpha) * idw_map

# Save blended map
pd.DataFrame(final_map, index=lats, columns=lons).to_csv('data/processed/radiation_blended_map.csv')

print('Kriging (all models), IDW, and blended maps computed and saved.')
