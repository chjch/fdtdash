import dash_mantine_components as dmc
from dash import html
import json

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
    return html.Div(
        id="arcgis-tools",
        children=arcgis_sketch_card,
        className="hidden",
    )


def get_building_visualization_card():
    return html.Div(
        id="building-visualization-card",
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
        # style={"margin": "10px"},
        className="cardChart arcgis_building_stats_card hidden",
    )


def get_basemap_gallery():
    basemap_gallery_card = dmc.Card(
        id="basemap-gallery-card",
        withBorder=True,
        shadow="sm",
        radius="md",
        children=[
            dmc.Text("Basemap Gallery", size="lg", className="chartLabel"),
            html.Div(id="basemap-gallery-card-content"),
        ],
    )
    return html.Div(
        id="drawer-basemap-gallery",
        className="mantine-Drawer-body-item hidden",
        children=[basemap_gallery_card],
    )


def get_arcgis_selection_widget_card():
    # ArcGIS Sketch Tool Card
    arcgis_selection_widget_card = dmc.Card(
        children=[
            dmc.Text("Building Selection Tool", size="lg", className="chartLabel arcgis-selection-card-label"),
            html.Div(
            html.Div([
                dmc.Button([
                    html.Div(
                        html.Img(src="/jtdash/assets/svg/clear_selection_icon16.svg",
                                 id="selection-tool-icon",
                                 className="selection-tool-icon"),
                    ),
                ],
                    variant="filled",
                    color="white",
                    className="clear-selection-tool-button button esri-sketch__section",
                    id="clear-selection-tool-button",

                    ),
            ],
                id="selection-widget-container",
                style={"height": "auto"}
            ),
                id="selection-widget-container-body"

            )
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        id="arcgis-selection-card",
        className="cardChart arcgis-sketch-card arcgis-selection-card"
    )

    return arcgis_selection_widget_card


def get_layer_texture_card():
    data = [
        ["original", "Buildings with original texture", "blue.6"],
        ["select", "Show commercial buildings", "violet.6"],
        ["emphasize", "Emphasize commercial buildings", "teal.6"],
        ["desaturate", "Desaturate texture", "yellow.6"],
        ["replace", "Remove texture", "gray.6"],
    ]

    radio_group = dmc.RadioGroup(
        children=dmc.Stack([dmc.Radio(l, value=k, color=c) for k, l, c in data], my=10),
        id="colorMixModeRadioGroup",
        value="original",
        label="Select building texture mode",
        size="sm",
        mt=10,
    )

    layer_texture_card = dmc.Card(
        children=[dmc.Text("Layer Texture Settings", size="lg"), radio_group],
        withBorder=True,
        shadow="sm",
        radius="md",
        id="layer_texture_card",
        className="cardChart layer-texture-card"
    )

    return layer_texture_card


def get_scene_layer_selection_card():
    # Data for each scene layer option
    data = [
        ["Downtown_Saint_Jones_River_SceneServer", "Downtown Saint Jones River", "blue.6"],
        ["Ribault_2_SceneServer", "Ribault 2", "violet.6"],
        ["Ribault_Scenic_Drive_Park_SceneServer", "Ribault Scenic Drive Park", "teal.6"],
        ["Hogen_Creek_Neighborhood_SceneServer", "Hogen Creek Neighborhood", "yellow.6"],
        ["demImageServer", "DEM Image Server", "gray.6"],
    ]

    # Create the radio group with options
    radio_group = dmc.RadioGroup(
        children=dmc.Stack([dmc.Radio(label, value=key, color=color) for key, label, color in data], my=10),
        id="sceneLayerRadioGroup",
        value="Downtown_Saint_Jones_River_SceneServer",
        label="Select Scene Layer",
        size="sm",
        mt=10,
    )

    # Define the card layout
    scene_layer_card = dmc.Card(
        children=[dmc.Text("Scene Layer Selection", size="lg"), radio_group],
        withBorder=True,
        shadow="sm",
        radius="md",
        id="scene_layer_card",
        className="cardChart scene-layer-card"
    )

    return scene_layer_card

import dash_mantine_components as dmc
from dash import dcc, html

def get_neighborhood_zoom_card():
    neighborhoods = {
        "Downtown": {"xmin": -81.663, "ymin": 30.321, "xmax": -81.640, "ymax": 30.340},
        "Riverside": {"xmin": -81.693, "ymin": 30.304, "xmax": -81.670, "ymax": 30.320},
        "San Marco": {"xmin": -81.667, "ymin": 30.290, "xmax": -81.645, "ymax": 30.310},
        # Add more neighborhoods with their extents as needed
    }

    # Create dropdown options from neighborhood names
    dropdown_options = [{"label": name, "value": name} for name in neighborhoods.keys()]

    # Dropdown for selecting neighborhoods
    dropdown = dcc.Dropdown(
        id="neighborhood-dropdown",
        options=dropdown_options,
        placeholder="Select a neighborhood...",
        style={"width": "100%"},
    )

    neighborhood_zoom_card = dmc.Card(
        children=[
            dmc.Text("Neighborhood Zoom Tool", size="lg", className="chartLabel"),
            dropdown,
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        id="neighborhood_zoom_card",
        className="cardChart neighborhood-zoom-card",

    )

    return neighborhood_zoom_card



global_widget_hover_card = dmc.Affix(
    children=get_arcgis_selection_widget_card(),
    position={"top": 0, "right": 10},
    zIndex=1000,
    id="selection-widget-hover-card-affix"
)