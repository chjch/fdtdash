import dash_mantine_components as dmc
from dash import html

def get_basemap_gallery():
    basemap_gallery_card = dmc.Card(
        id="basemap-gallery-card",
        withBorder=True,
        shadow="sm",
        radius="md",
        children=[
            dmc.Text("Basemap Gallery", size="lg", className="chartLabel"),
            # Basemap gallery widget will render to this div from main.defer
            html.Div(id="basemap-gallery-card-content"),
        ],
    )

    basemap_gallery = html.Div(
        id="basemap-gallery",
        children=[basemap_gallery_card],
    )
    
    return basemap_gallery