from branca.colormap import linear
from branca.element import Template, MacroElement

def create_colormap(gdf):
    colormap = linear.YlOrRd_09.scale(
        gdf["capacity_mwp"].min(), gdf["capacity_mwp"].max()
    )
    colormap.caption = "Installed Solar Capacity (MWp)"
    return colormap

def create_custom_legend(colormap):
    legend_html = f"""
    {{% macro html(this, kwargs) %}}
    <div style='
        position: fixed;
        bottom: 50px;
        left: 20px;
        z-index: 9999;
        background-color: white;
        padding: 10px;
        border: 2px solid grey;
        border-radius: 5px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    '>
        <h4 style="margin: 0;">{colormap.caption}</h4>
        {colormap._repr_html_()}
    </div>
    {{% endmacro %}}
    """

    macro = MacroElement()
    macro._template = Template(legend_html)
    return macro
