"""modified from the original app.py"""
import dash
import pathlib
from dash import Dash, html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask
from dash_extensions import DeferScript, EventListener
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .layout import html_layout
from .linecharts import means_to_work
# from .sidebar import sidebar, collapse_button
from .sidebar2 import sidebar2

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
    {"src": "https://unpkg.com/@mantine/charts@7/styles.css"},
    {"src":  "https://unpkg.com/@mantine/dates@7/styles.css"},
]


def init_dashboard(server: Flask):
    """Create a Plotly Dash dashboard within a running Flask jtflask."""

    dash._dash_renderer._set_react_version('18.2.0')

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
                DeferScript(src="../static/assets/js/main-defer.js"),
                html.Div(id="deckgl-container"),
                sidebar2(dash_app),
                # Additional components
            ]
        )
    )

    @dash_app.callback(
        [
            Output("chart_scrollable_drawer", "opened"),
            Output("drawer", "size"),
            Output("collapse-icon", "icon")
        ],
        Input("collapse-button", "n_clicks"),
        State("chart_scrollable_drawer", "opened"),
        prevent_initial_call=True,
    )
    def toggle_drawer_and_size(n_clicks, is_open):
        new_size = "auto" if is_open else "md"
        new_icon = "heroicons:chevron-double-right-16-solid" if is_open else "heroicons:chevron-double-left-16-solid"
        return not is_open, new_size, new_icon

    return dash_app.server
