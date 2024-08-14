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
from .statsHoverCards import stats_hover_card
# from .charts import create_charts
from .arcgisJS_tools import get_arcgis_sketch_card
from .sidebar2 import sidebar2, get_sidebar_components

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
    {"src":  "https://unpkg.com/@mantine/dates@7/styles.css"}
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
                stats_hover_card
                # use dcc store for buildings selection json
                # dcc.Store()
            ]
        )
    )
    # get sidebar components
    sidebar_brand, sidebar_main_container, collapse_button_container, scrollable_div_charts, scrollable_div_tools = get_sidebar_components(dash_app)

    # Collapse Chart Callback
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

    # toggle drawer content, ----not working----

    @dash_app.callback(
        Output("chart_scrollable_drawer", "children"),
        Output("drawer-content-store", "data"),
        [Input("open-charts-drawer-link", "n_clicks"),
         Input("open-arcgis-drawer-link", "n_clicks")],
        [State('drawer-content-store', 'data')]
    )
    def update_drawer_content(charts_click, tools_click, current_content):
        ctx = dash.callback_context

        print(f"Triggered: {ctx.triggered}")
        print(f"Charts Clicked: {charts_click}, Tools Clicked: {tools_click}")
        print(f"Current Content: {current_content}")

        if not ctx.triggered:
            return no_update, no_update

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == "open-charts-drawer-link" and current_content != 'charts':
            print("Switching to Charts Content")
            return scrollable_div_charts, 'charts'
        elif trigger_id == "open-arcgis-drawer-link" and current_content != 'tools':
            print("Switching to Tools Content")
            return scrollable_div_tools, 'tools'

        return no_update, no_update

    # @dash_app.callback(
    #     Output("chart_scrollable_drawer", "children"),
    #     [Input("open-charts-drawer-link", "n_clicks"),
    #      Input("open-arcgis-drawer-link", "n_clicks")],
    #     [State('drawer-content-store', 'data')]
    # )
    # def update_drawer_content(charts_click, tools_click, current_content):
    #     ctx = dash.callback_context
    #
    #     print(f"Triggered: {ctx.triggered}")
    #     print(f"Charts Clicked: {charts_click}, Tools Clicked: {tools_click}")
    #     print(f"Current Content: {current_content}")
    #
    #     if not ctx.triggered:
    #         print("No input triggered the callback.")
    #         return no_update
    #
    #     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    #     print(f"Triggered by: {trigger_id}")
    #
    #     if trigger_id == "open-charts-drawer-link" and current_content != 'charts':
    #         print("Switching to Charts Content")
    #         return [html.Div(id="chart_scrollable_div")], 'charts'
    #     elif trigger_id == "open-arcgis-drawer-link" and current_content != 'tools':
    #         print("Switching to Tools Content")
    #         return [html.Div(id="chart_scrollable_div")], 'tools'
    #
    #     return no_update


    # selected buildings Callback
    selected_buildings = []

    # @dash_app.sever.route('/jtdash/selection', methods=['POST'])
    # def selection():
    #     global selected_buildings
    #     selected_buildings = request.json['buildings']
    #     return jsonify({"status": "success"})
    #
    # @dash_app.callback(
    #     Output('chart-id', 'figure'),
    #     [Input('interval-component', 'n_intervals')]
    # )
    # def update_chart(n_intervals):
    #     global selected_buildings
    #     if not selected_buildings:
    #         raise PreventUpdate
    #
    #     # Process selected_buildings and update the chart
    #     # ...
    #     updated_figure = None
    #
    #     return updated_figure

    return dash_app.server