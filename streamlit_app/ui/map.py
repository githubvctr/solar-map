def build_map(gdf, colormap, filtered, enable_selection=False):
    import folium
    from folium import GeoJson, GeoJsonTooltip
    from shapely.geometry import Point
    import numpy as np
    from branca.colormap import StepColormap

    # Calculate area in km² for each municipality
    gdf = gdf.copy()
    gdf["area_km2"] = gdf.geometry.to_crs(epsg=3857).area / 1e6
    gdf["density"] = gdf["Installaties (aantal)"] / gdf["area_km2"]
    filtered = gdf.loc[filtered.index]

    m = folium.Map(location=[52.1, 5.2], zoom_start=7)

    # Use quantiles for density
    values = filtered["density"].values
    quantiles = np.quantile(values, [0, 0.2, 0.4, 0.6, 0.8, 1.0])
    bins = list(sorted(set(quantiles)))
    step_colormap = StepColormap(
        colors=["#ffffb2", "#fecc5c", "#fd8d3c", "#f03b20", "#bd0026"],
        vmin=min(values),
        vmax=max(values),
        index=bins,
        caption=None
    )

    def style_function(feature):
        density = feature["properties"]["density"]
        return {
            "fillColor": step_colormap(density),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        }

    gj = folium.GeoJson(
        filtered[["Name", "Installaties (aantal)", "area_km2", "density", "geometry"]].__geo_interface__,
        name="Municipalities",
        style_function=style_function,
        tooltip=GeoJsonTooltip(
            fields=["Name", "Installaties (aantal)", "area_km2", "density"],
            aliases=["Municipality", "Installations", "Area (km²)", "Installations/km²"],
            localize=True,
            digits=2
        )
    )

    gj.add_to(m)
    # Add custom legend for density per km² with quantile percentages
    legend_html = f'''
     <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 270px; height: 180px; 
                 background-color: black; z-index:9999; font-size:14px; border:2px solid grey; border-radius:8px; padding: 10px; color: white;">
     <b>Installations per km²</b><br>
     <i>Color bins (quantiles):</i><br>
     <span style="background:#ffffb2;display:inline-block;width:20px;height:10px;"></span> 0–20% (Lowest)<br>
     <span style="background:#fecc5c;display:inline-block;width:20px;height:10px;"></span> 20–40%<br>
     <span style="background:#fd8d3c;display:inline-block;width:20px;height:10px;"></span> 40–60%<br>
     <span style="background:#f03b20;display:inline-block;width:20px;height:10px;"></span> 60–80%<br>
     <span style="background:#bd0026;display:inline-block;width:20px;height:10px;"></span> 80–100% (Highest)<br>
     </div>
     '''
    m.get_root().html.add_child(folium.Element(legend_html))
    return m
