import dash_mantine_components as dmc
from dash import html
from .widgets import get_arcgis_sketch_card

def get_tools():
    arcgis_sketch_tool_card = get_arcgis_sketch_card()

    return html.Div(
        id="arcgis-tools",
        children=[arcgis_sketch_tool_card],
    )
   