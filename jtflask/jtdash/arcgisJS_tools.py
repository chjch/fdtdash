import dash_mantine_components as dmc
from dash import html, dcc


def get_arcgis_sketch_card():
    # ArcGIS Sketch Tool Card
    arcgis_sketch_card = dmc.Card(
        children=[
            dmc.Text("ArcGIS Sketch Tool", size="lg", className="chartLabel"),
            html.Div(id="arcgis-sketch-container", style={"height": "100px"})
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"margin": "10px"},
        id="arcgis_sketch_card",
        className="cardChart"
    )

    return arcgis_sketch_card