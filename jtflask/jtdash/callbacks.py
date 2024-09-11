import dash
from dash import Input, Output, State, no_update


def register_callbacks(dashboard):
    @dashboard.callback(
        [
            Output("chart_scrollable_div", "className"),
            Output("arcgistools_scrollable_div", "className"),
            Output("scrollable_div_basemapGallery", "className"),
            Output("scrollable_div_bulding_stats", "className"),  # Output for buildings
            Output("chart_scrollable_div", "style"),
            Output("arcgistools_scrollable_div", "style"),
            Output("scrollable_div_basemapGallery", "style"),
            Output("scrollable_div_bulding_stats", "style"),  # Style for buildings
            Output("drawer-content-store", "data"),
            Output("drawer", "style"),  # Added Output for drawer style
        ],
        [
            Input("open-charts-drawer-link", "n_clicks"),
            Input("open-arcgis-drawer-link", "n_clicks"),
            Input("open-basemaps-link", "n_clicks"),
            Input("open-buildings-link", "n_clicks"),  # Input for buildings
        ],
        [State("drawer-content-store", "data")],
        prevent_initial_call=True,
    )
    def update_drawer_content(charts_click, tools_click, basemaps_click, buildings_click, current_content):
        ctx = dash.callback_context

        if not ctx.triggered:
            return (no_update,) * 10  # Updated to return 10 outputs

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # List of sidebar icon NavLinks that should trigger the callback
        valid_navlinks = [
            "open-charts-drawer-link",
            "open-arcgis-drawer-link",
            "open-basemaps-link",
            "open-buildings-link",
        ]

        # Only execute if the trigger is a sidebar icon NavLink
        if trigger_id not in valid_navlinks:
            return (no_update,) * 10

        # Handle charts drawer case
        if trigger_id == "open-charts-drawer-link" and current_content != "charts":
            return (
                "slide-in",  # Show charts
                "slide-out",  # Hide ArcGIS tools
                "slide-out",  # Hide basemaps
                "slide-out",  # Hide buildings
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                "charts",
                {},  # Revert drawer style to default
            )

        # Handle ArcGIS tools drawer case
        elif trigger_id == "open-arcgis-drawer-link" and current_content != "tools":
            return (
                "slide-out",  # Hide charts
                "slide-in",  # Show ArcGIS tools
                "slide-out",  # Hide basemaps
                "slide-out",  # Hide buildings
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},
                "tools",
                {},  # Revert drawer style to default
            )

        # Handle basemaps drawer case
        elif trigger_id == "open-basemaps-link" and current_content != "basemaps":
            return (
                "slide-out",  # Hide charts
                "slide-out",  # Hide ArcGIS tools
                "slide-in",  # Show basemaps
                "slide-out",  # Hide buildings
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},
                "basemaps",
                {},  # Revert drawer style to default
            )

        # Handle buildings drawer case
        elif trigger_id == "open-buildings-link" and current_content != "buildings":
            return (
                "slide-out",  # Hide charts
                "slide-out",  # Hide ArcGIS tools
                "slide-out",  # Hide basemaps
                "slide-in",  # Show buildings
                {"display": "none"},
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},
                "buildings",
                {"width": "800px !important"},  # Set drawer width to 500px
            )

        return (no_update,) * 10  # Updated to return 10 outputs

    # Collapse Sidebar Callback
    @dashboard.callback(
        [
            Output("chart_scrollable_drawer", "opened"),
            Output("collapse-icon", "icon"),
        ],
        Input("collapse-button", "n_clicks"),
        State("chart_scrollable_drawer", "opened"),
        prevent_initial_call=True,
    )
    def toggle_drawer_and_size(n_clicks, is_open):
        new_icon = (
            "heroicons:chevron-double-right-16-solid"
            if is_open
            else "heroicons:chevron-double-left-16-solid"
        )
        return not is_open, new_icon

    # Scenario Chart callback
    @dashboard.callback(
        Output("yearSelectValue", "children"), Input("yearSelect", "value")
    )
    def select_value(value):
        return value

    @dashboard.callback(
        Output("stormSelectValue", "children"), Input("stormSelect", "value")
    )
    def select_value(value):
        return value


    # @dashboard.callback(
    #     Output('eff-yr-blt-chart', 'data'),
    #     Input('buildings-data', 'data')  #  data is stored in dcc.Store
    # )
    # def update_eff_yr_blt_chart(data):
    #     return {
    #         "labels": ["<1950", "1950-1975", "1975-2000", ">2000"],
    #         "datasets": [{
    #             "label": "Effective Year Built",
    #             "data": data,  # The data from the Flask response
    #             "backgroundColor": "#149dcf"
    #         }]
    #     }

    @dashboard.callback(
        Output('eff-yr-blt-chart', 'data'),
        Output('tot-lvg-area-chart', 'data'),
        Output('just-value-chart', 'data'),
        Input('building-stats-store', 'data')  # Assuming the data is stored in a Store component
    )
    def update_building_stats_charts(data):
        if data is None:
            return [], [], []

        # Update the Effective Year Built chart
        eff_yr_blt_data = [
            {"year": "<1950", "count": data['pre_1950']},
            {"year": "1950-1975", "count": data['1950_1975']},
            {"year": "1975-2000", "count": data['1975_2000']},
            {"year": ">2000", "count": data['post_2000']}
        ]

        # Update the Total Living Area chart
        tot_lvg_area_data = [
            {"area": "<1000 sq ft", "count": data['TOTLVGAREA'] < 1000},
            {"area": "1000-2000 sq ft", "count": 1000 <= data['TOTLVGAREA'] <= 2000},
            {"area": "2000-3000 sq ft", "count": 2000 <= data['TOTLVGAREA'] <= 3000},
            {"area": ">3000 sq ft", "count": data['TOTLVGAREA'] > 3000}
        ]

        # Update the Just Value chart
        just_value_data = [
            {"value": "<$100k", "count": data['JV'] < 100000},
            {"value": "$100k-$500k", "count": 100000 <= data['JV'] <= 500000},
            {"value": "$500k-$1M", "count": 500000 <= data['JV'] <= 1000000},
            {"value": ">$1M", "count": data['JV'] > 1000000}
        ]

        return eff_yr_blt_data, tot_lvg_area_data, just_value_data