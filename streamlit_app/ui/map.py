def build_map(gdf, colormap, filtered, enable_selection=False):
    import folium
    from folium import GeoJson, GeoJsonTooltip
    from shapely.geometry import Point

    m = folium.Map(location=[52.1, 5.2], zoom_start=7)

    # Function to apply style
    def style_function(feature):
        capacity = feature["properties"]["capacity_mwp"]
        return {
            "fillColor": colormap(capacity),
            "color": "black",
            "weight": 0.5,
            "fillOpacity": 0.7,
        }

    # Add GeoJson polygons with tooltip
    gj = folium.GeoJson(
        filtered[["Name", "capacity_mwp", "geometry"]].__geo_interface__,
        name="Municipalities",
        style_function=style_function,
        tooltip=GeoJsonTooltip(
            fields=["Name", "capacity_mwp"],
            aliases=["Municipality", "Installed MWp"],
            localize=True,
        )
    )

    gj.add_to(m)

    #colormap.add_to(m)
    return m
