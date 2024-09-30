import dash_mantine_components as dmc
from dash import html


def get_arcgis_sketch_card():
    # ArcGIS Sketch Tool Card
    arcgis_sketch_card = dmc.Card(
        children=[
            dmc.Text("ArcGIS Sketch Tool", size="lg", className="chartLabel"),
            html.Div(id="arcgis-sketch-container", style={"height": "100px"}),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        id="arcgis_sketch_card",
        className="cardChart",
    )
    return arcgis_sketch_card


def get_arcgis_building_stats_card():
    # ArcGIS Building Stats Tool Card
    arcgis_building_stats_card = dmc.Card(
        children=[
            dmc.Text("Building Statistics", size="lg", className="chartLabel"),
            # Tool widget in its own card
            dmc.Card(
                children=[
                    dmc.Text(
                        "Buildings Color View",
                        size="md",
                        className="toolLabel",
                    ),
                    dmc.Group(
                        children=[
                            dmc.Button(
                                "DORUC",
                                id="doruc-button",
                                variant="gradient",
                                gradient={"from": "#3613b8", "to": "#5932EA"},
                                className="buildings-view-tool-button",
                            ),
                            dmc.Button(
                                "EFFYRBLT",
                                id="effyrblt-button",
                                variant="gradient",
                                gradient={"from": "#3613b8", "to": "#5932EA"},
                                className="buildings-view-tool-button",
                            ),
                            dmc.Button(
                                "LIVINGAREA",
                                id="totlvgarea-button",
                                variant="gradient",
                                gradient={"from": "#3613b8", "to": "#5932EA"},
                                className="buildings-view-tool-button",
                            ),
                            dmc.Button(
                                "JUSTVALUE",
                                id="justvalue-button",
                                variant="gradient",
                                gradient={"from": "#3613b8", "to": "#5932EA"},
                                className="buildings-view-tool-button",
                            ),
                        ],
                        align="center",  # Align buttons in the center
                        gap="md",  # Gap between buttons
                        className="buildings-view-tool-buttons",
                    ),
                    html.Div(
                        id="buffer-slider-container",
                        style={"margin-top": "20px"},
                    ),
                    # Placeholder for buffer slider
                    dmc.Button(
                        "Reset Color",
                        id="reset-color-button",
                        variant="filled",
                        color="gray",
                        className="reset-color-button",
                    ),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                style={
                    "padding": "16px",
                    "margin-bottom": "20px",
                },  # Set padding and margin
                className="cardChart toolCard",
            ),
            dmc.Card(
                children=[
                    dmc.Text(
                        "Highlight Categories",
                        size="md",
                        className="toolLabel",
                    ),
                    dmc.Group(
                        children=[
                            dmc.Button(
                                "Residential",
                                id="highlight-residential",
                                variant="light",
                                color="yellow",
                                className="highlight-category-button",
                            ),
                            dmc.Button(
                                "Retail-Office",
                                id="highlight-retail",
                                variant="light",
                                color="blue",
                                className="highlight-category-button",
                            ),
                            dmc.Button(
                                "Industrial",
                                id="highlight-industrial",
                                variant="light",
                                color="purple",
                                className="highlight-category-button",
                            ),
                            dmc.Button(
                                "Vacant-Nonresidential",
                                id="highlight-vacant",
                                variant="light",
                                color="red",
                                className="highlight-category-button",
                            ),
                            dmc.Button(
                                "Agricultural",
                                id="highlight-agricultural",
                                variant="light",
                                color="green",
                                className="highlight-category-button",
                            ),
                        ],
                        align="center",
                        gap="md",
                        className="highlight-category-buttons",
                    ),
                ],
                shadow="sm",
                radius="md",
                withBorder=True,
                style={"padding": "16px", "margin-bottom": "20px"},
                className="cardChart highlightCard",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"margin": "10px"},
        className="cardChart arcgis_building_stats_card",
    )
    return arcgis_building_stats_card
