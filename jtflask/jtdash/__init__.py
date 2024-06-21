"""modified from the original app.py"""

import pathlib
from dash import Dash, html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask
from dash_extensions import DeferScript, EventListener
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .layout import html_layout
from .linecharts import means_to_work
from .sidebar import sidebar, collapse_button

external_scripts = [
    {"src": "https://unpkg.com/@loaders.gl/i3s@3.3.1/dist/dist.min.js"},
    {"src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"},
    {"src": "https://unpkg.com/@turf/turf@6/turf.min.js"},
]

external_stylesheets = [
    {
        "src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css",
        "rel": "stylesheet",
    },
]

def init_dashboard(server: Flask):
    """Create a Plotly Dash dashboard within a running Flask jtflask."""
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/jtdash/",
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        assets_folder=str(
            pathlib.Path(__file__).parent.parent / "static/assets"
        ),
        assets_ignore=".*defer.js$",
    )
    dash_app.index_string = html_layout

    event = {"event": "click", "props": ["srcElement.parentElement.dataset.geoid20"]}

    dash_app.layout = dmc.MantineProvider(
        html.Div(
            [
                DeferScript(src="../static/assets/js/arcgis-defer.js"),
                html.Div(id="deckgl-container"),
                sidebar(),  # Include the sidebar drawer
                # Additional components
            ]
        )
    )

    @dash_app.callback(
        [Output("drawer", "size"),
         Output("sidebar-col1", "style"),
         Output("collapse-button-container", "style"),
         Output("collapse-icon", "icon")],
        Input("collapse-button", "n_clicks"),
        State("drawer", "size"),
        prevent_initial_call=True,
    )
    def toggle_drawer_size(n_clicks, current_size):
        if current_size == "80px":
            return ("15px", {"display": "none"},
                    {"height": "100%", "width": "100%", "backgroundColor": "lightgray", "display": "flex",
                     "alignItems": "center", "justifyContent": "center"},
                    "akar-icons:chevron-right")
        else:
            return ("80px", {"display": "block"},
                    {"height": "100%", "width": "15px", "backgroundColor": "lightgray", "display": "flex",
                     "alignItems": "center", "justifyContent": "center"},
                    "akar-icons:chevron-left")

    return dash_app.server
