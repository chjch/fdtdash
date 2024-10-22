import pathlib
from flask import Flask
import dash

from .layout import layout, html_layout
from .callbacks import register_callbacks

external_scripts = [
    # {"src": "https://unpkg.com/@loaders.gl/i3s@3.3.1/dist/dist.min.js"},
    # {"src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"},
    # {"src": "https://unpkg.com/@turf/turf@6/turf.min.js"},
]
external_stylesheets = [
    # {
    #     "src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css",
    #     "rel": "stylesheet",
    # },
    {"src": "https://unpkg.com/@mantine/charts@7/styles.css"},
    {"src": "https://unpkg.com/@mantine/dates@7/styles.css"},
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"},
]


def init_dashboard(server: Flask):
    dash._dash_renderer._set_react_version("18.2.0")  # noqa setting react version for dmc

    dashboard = dash.Dash(
        server=server,
        routes_pathname_prefix="/jtdash/",
        external_stylesheets=external_stylesheets,
        external_scripts=external_scripts,
        assets_folder=str(
            pathlib.Path(__file__).parent.parent / "static/assets"
        ),
        assets_ignore=".*defer.js$",
        title="JaxTwin: An Urban Digital Twin for Jacksonville",
    )
    dashboard.index_string = html_layout(with_splash=True)
    dashboard.layout = layout
    # dashboard.enable_dev_tools(debug=True)
    register_callbacks(dashboard)
    return dashboard.server
