"""modified from the original app.py"""

import pathlib
from dash import Dash, html, dcc, callback, Input, Output, State
from dash.exceptions import PreventUpdate
from flask import Flask
from dash_extensions import DeferScript, EventListener
import dash_mantine_components as dmc
from dash_iconify import DashIconify
# import dash_bootstrap_components as dbc

from .layout import html_layout
from .linecharts import means_to_work
from .sidebar import sidebar

external_scripts = [
    {"src": "https://unpkg.com/deck.gl@8.9.35/dist.min.js"},
    {"src": "https://unpkg.com/@loaders.gl/i3s@3.3.1/dist/dist.min.js"},
    {"src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"},
    {"src": "https://unpkg.com/@turf/turf@6/turf.min.js"},
    # {"src": "../static/assets/js/arcgis-defer.js", "defer": True},
    # {"src": "{{ url_for('static', filename='node_modules/@loaders.gl/i3s/dist/index.js') }}"}
]
external_stylesheets = [
    {
        "src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css",
        "rel": "stylesheet",
    },
    # {
    #     "href": "https://js.arcgis.com/4.29/esri/themes/light/main.css",
    #     "rel": "stylesheet",
    #     "type": "text/css",
    # }
]


def init_dashboard(server: Flask):
    """Create a Plotly Dash dashboard within a running Flask jtflask."""
    # Embed a Dash app into a Flask `server`
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
    # dmc_card = dmc.Card(
    #     children=[
    #         html.Div(children="Means to Work", id="means-to-work-title"),
    #         dcc.Graph(
    #             id="mean-to-work-line-chart",
    #             responsive=True,
    #             config={"displayModeBar": False},
    #         ),
    #     ],
    #     withBorder=True,
    #     shadow="sm",
    #     radius="md",
    #     style={
    #         "width": 500,
    #         "height": 250,
    #         "zIndex": 100,
    #         "position": "absolute",
    #         "bottom": 20,
    #         "left": 20,
    #     },
    # )
    # JavaScript event(s) that we want to listen to and what properties to collect.
    event = {"event": "click", "props": ["srcElement.parentElement.dataset.geoid20"]}
    dash_app.layout = dmc.MantineProvider(
        html.Div(
            [
                DeferScript(src="../static/assets/js/arcgis-defer.js",),
                html.Div(id="deckgl-container"),
                sidebar(),
                # EventListener(
                #     html.Div(id="deckgl-container", **{"data-geoid20": ""}),
                #     events=[event],
                #     # logging=True,
                #     id="deckgl-container-el",
                # ),
                # dmc_card,
                # dcc.Input(id="GEOID20", value="", type="text"),
            ]
        )
    )

    # @callback(
    #     Output("mean-to-work-line-chart", "figure"),
    #     Input("deckgl-container-el", "n_events"),
    #     State("deckgl-container-el", "event"),
    # )
    # def update_means_to_work_line_chart(n_events, e):
    #     if e is None:
    #         raise PreventUpdate()
    #     print("callback triggered!")
    #     print(e)
    #     print(type(e["srcElement.parentElement.dataset.geoid20"]))
    #     return means_to_work(e["srcElement.parentElement.dataset.geoid20"])

    return dash_app.server
