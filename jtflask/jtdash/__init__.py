"""modified from the original app.py"""
import dash
import pathlib
from dash import Dash, html, dcc, callback, Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from flask import Flask, request, jsonify
from dash_extensions import DeferScript, EventListener
import dash_mantine_components as dmc
from .layout import html_layout
from .linecharts import means_to_work
from .statshovercards import stats_hover_card
# from .charts import create_charts
from .arcgis_JS_tools import get_arcgis_sketch_card
from .sidebar import sidebar, get_sidebar_components

global_sidebar_brand = None
global_sidebar_main_container = None
global_collapse_button_container = None
global_scrollable_div_charts = None
global_scrollable_div_tools = None
global_scrollable_div_hidden = None

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
    {"src": "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"}
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

    # Initialize sidebar components and store as globals
    (global_sidebar_brand, global_sidebar_main_container,
     global_collapse_button_container, global_scrollable_div_charts,
     global_scrollable_div_tools) = get_sidebar_components()

    dash_app.layout = dmc.MantineProvider(
        html.Div(
            [
                DeferScript(src="../static/assets/js/main-defer.js"),
                html.Div(id="deckgl-container"),
                EventListener(
                    id="arcgis-event-listener",
                    events=[{"event": "restore-sketch-tool"},
                            {"event": "hide-sketch-tool"}]),
                dcc.Store(id="arcgis-tool-state"),
                # EventListener(
                #     id="arcgis-event-listener",
                #     events=[{"event": "arcgis-tool-initialized"}],
                #     logging=True
                # ),
                # dcc.Store(id='arcgis-tool-state', data={}),
                sidebar(dash_app, global_sidebar_brand, global_sidebar_main_container,
                        global_collapse_button_container, global_scrollable_div_charts,
                        global_scrollable_div_tools),

                stats_hover_card
                # use dcc store for buildings selection json?
                # dcc.Store()
            ]
        )
    )

    @dash_app.callback(
        [Output("chart_scrollable_div", "className"),
         Output("arcgistools_scrollable_div", "className"),
         Output("chart_scrollable_div", "style"),
         Output("arcgistools_scrollable_div", "style"),
         Output("drawer-content-store", "data")],
        [Input("open-charts-drawer-link", "n_clicks"),
         Input("open-arcgis-drawer-link", "n_clicks")],
        [State('drawer-content-store', 'data')],
        prevent_initial_call=True
    )
    def update_drawer_content(charts_click, tools_click, current_content):
        ctx = dash.callback_context

        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == "open-charts-drawer-link" and current_content != 'charts':
            # Show the charts div with slide-in animation, hide the tools div
            return "slide-in", "slide-out", {"display": "block"}, {"display": "none"}, "charts"

        elif trigger_id == "open-arcgis-drawer-link" and current_content != 'tools':
            # Show the tools div with slide-in animation, hide the charts div
            return "slide-out", "slide-in", {"display": "none"}, {"display": "block"}, "tools"

        return no_update, no_update, no_update, no_update, no_update


    # Collapse Sidebar Callback
    @dash_app.callback(
        [
            Output("chart_scrollable_drawer", "opened"),
            Output("drawer", "size"),
            Output("collapse-icon", "icon"),


        ],
        Input("collapse-button", "n_clicks"),
        State("chart_scrollable_drawer", "opened"),
        prevent_initial_call=True,
    )
    def toggle_drawer_and_size(n_clicks, is_open):
        new_size = "auto" if is_open else "md"
        new_icon = "heroicons:chevron-double-right-16-solid" if is_open else "heroicons:chevron-double-left-16-solid"
        return not is_open, new_size, new_icon

    # Scenario Chart callback
    @dash_app.callback(Output("yearSelectValue", "children"),
                       Input("yearSelect", "value"))
    def select_value(value):
        return value

    @dash_app.callback(Output("stormSelectValue", "children"),
                       Input("stormSelect", "value"))
    def select_value(value):
        return value


    return dash_app.server