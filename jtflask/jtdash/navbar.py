from dash import html, dcc
import dash_mantine_components as dmc
from .brand import get_brand
from .charts import get_charts
from .widgets import (
    get_arcgis_sketch_card,
    get_building_visualization_card,
    get_basemap_gallery,
)
from .utils import get_icon

NAVBAR_BUTTONS = {
    "charts": "charts-button",
    "hazard": "tools-button",
    "housing": "buildings-toggle-button",
    "health": "layers-toggle-button",
    "neighborhood": "clipboard-toggle-button",
    "legend": "legend-toggle-button",
    "basemap": "basemaps-gallery-button",
    "collapse": "collapse-button",
}

NAVBAR_PANELS = {
    "charts": get_charts(),
    "hazard": get_arcgis_sketch_card(),
    "housing": get_building_visualization_card(),
    "health": dmc.Card("Health", id="health-panel", className="hidden"),
    "neighborhood": dmc.Card("Neighborhood", id="neighborhood-panel", className="hidden"),
    "legend": dmc.Card("Legend", id="legend-panel", className="hidden"),
    "basemap": get_basemap_gallery(),
}


def get_navbar_buttons():
    return html.Div(
        id="navbar-buttons",
        children=[
            dmc.Button(
                id=NAVBAR_BUTTONS["charts"],
                children=get_icon(icon="carbon:chart-line-data"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["hazard"],
                children=get_icon("carbon:flood", "open-arcgis"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["housing"],
                children=get_icon("ph:buildings"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["health"],
                children=get_icon("fluent-mdl2:health"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["neighborhood"],
                children=get_icon("ph:park-light"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["legend"],
                children=html.Div(id="legend-svg"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["basemap"],
                children=html.Div(id="basemap-svg"),
                className="navbar-button",
            ),
        ],
    )


def get_navbar_collapse_button():
    return dmc.Button(
        id=NAVBAR_BUTTONS["collapse"],
        children=[
            get_icon(
                icon="heroicons:chevron-double-left-16-solid",
                icon_id="collapse-icon",
            )
        ],
        variant="default",
        fullWidth=False,
    )


def get_navbar_controls():  # Navbar Control: brand, buttons, collapse button
    navbar_brand = get_brand()
    navbar_buttons = get_navbar_buttons()
    navbar_collapse = html.Div(
        id="collapse-button-container",
        children=get_navbar_collapse_button(),
    )
    return html.Div(
        id="navbar-control",
        children=[navbar_brand, navbar_buttons, navbar_collapse],
    )


def get_navbar_panels():
    return html.Div(
        id="navbar-drawer",
        children=[*NAVBAR_PANELS.values()],
    )
