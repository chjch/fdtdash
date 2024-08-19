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

global_sidebar_brand = None
global_sidebar_main_container = None
global_collapse_button_container = None
global_scrollable_div_charts = None
global_scrollable_div_tools = None

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

    # Initialize the sidebar components once and store them in global variables
    (global_sidebar_brand, global_sidebar_main_container,
     global_collapse_button_container, global_scrollable_div_charts,
     global_scrollable_div_tools) = get_sidebar_components()

    dash_app.layout = dmc.MantineProvider(
        html.Div(
            [
                DeferScript(src="../static/assets/js/main-defer.js"),
                html.Div(id="deckgl-container"),
                sidebar2(dash_app, global_sidebar_brand, global_sidebar_main_container,
                         global_collapse_button_container, global_scrollable_div_charts,
                         global_scrollable_div_tools),
                EventListener(
                    id="arcgis-event-listener",
                    events=[{"event": "arcgis-tool-initialized"}],
                    logging=True  # Optional: Enable logging for debugging
                ),
                dcc.Store(id='arcgis-tool-state', data={}),
                stats_hover_card
                # use dcc store for buildings selection json
                # dcc.Store()
            ]
        )
    )

    # get sidebar components
    # sidebar_brand, sidebar_main_container, collapse_button_container, scrollable_div_charts, scrollable_div_tools = get_sidebar_components(dash_app)

    # save tool state
    @dash_app.callback(
        Output('arcgis-tool-state', 'data'),
        Input('arcgis-event-listener', 'event')
    )
    def save_arcgis_tool_state(event):
        # Logic to extract the state of the ArcGIS tool and store it
        tool_state = {"initialized": True}  # Example state, modify as per your tool's state
        return tool_state

    # toggle navlinks charts with state
    @dash_app.callback(
        Output("chart_scrollable_drawer", "children"),
        Output("drawer-content-store", "data"),
        [Input("open-charts-drawer-link", "n_clicks"),
         Input("open-arcgis-drawer-link", "n_clicks"),
         ],
        [State('drawer-content-store', 'data'),
         State('arcgis-tool-state', 'data')],
        prevent_initial_call = True
    )
    def update_drawer_content(charts_click, tools_click, current_content, arcgis_tool_state):
        ctx = dash.callback_context

        if not ctx.triggered:
            return no_update, no_update

        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if trigger_id == "open-charts-drawer-link" and current_content != 'charts':
            return global_scrollable_div_charts, 'charts'
        elif trigger_id == "open-arcgis-drawer-link" and current_content != 'tools':
            # If ArcGIS tool was initialized before, reinitialize it
            # if arcgis_tool_state.get('initialized'):
            #     reinitialize_arcgis_tool_js = "initializeArcGISTool();"  # Custom JS logic to reinitialize
            #     return [
            #         global_scrollable_div_tools,
            #         # dcc.Interval(id='reinit-sketch', interval=1, n_intervals=0),
            #         dcc.Markdown(f'<script>{reinitialize_arcgis_tool_js}</script>', dangerously_allow_html=True)
            #     ], 'tools'
            return global_scrollable_div_tools, 'tools'
        return no_update, no_update

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