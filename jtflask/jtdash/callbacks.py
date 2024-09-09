import dash
from dash import Input, Output, State, no_update


def register_callbacks(dashboard):
    @dashboard.callback(
        [
            Output("chart_scrollable_div", "className"),
            Output("arcgistools_scrollable_div", "className"),
            Output("scrollable_div_basemapG", "className"),  # Added output for basemaps
            Output("chart_scrollable_div", "style"),
            Output("arcgistools_scrollable_div", "style"),
            Output("scrollable_div_basemapG", "style"),  # Added style for basemaps
            Output("drawer-content-store", "data"),
        ],
        [
            Input("open-charts-drawer-link", "n_clicks"),
            Input("open-arcgis-drawer-link", "n_clicks"),
            Input("open-basemaps-link", "n_clicks"),  # Added input for basemaps
        ],
        [State("drawer-content-store", "data")],
        prevent_initial_call=True,
    )
    def update_drawer_content(charts_click, tools_click, basemaps_click, current_content):
        ctx = dash.callback_context

        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # List of sidebar icon NavLinks that should trigger the callback
        valid_navlinks = [
            "open-charts-drawer-link",
            "open-arcgis-drawer-link",
            "open-basemaps-link"  # Added basemaps link to valid_navlinks
        ]

        # Only execute if the trigger is a sidebar icon NavLink
        if trigger_id not in valid_navlinks:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        if trigger_id == "open-charts-drawer-link" and current_content != "charts":
            return (
                "slide-in",
                "slide-out",
                "slide-out",  # Add a default or placeholder class for basemaps
                {"display": "block"},
                {"display": "none"},
                {"display": "none"},  # Hides basemaps
                "charts",
            )

        elif trigger_id == "open-arcgis-drawer-link" and current_content != "tools":
            return (
                "slide-out",
                "slide-in",
                "slide-out",  # Add a default or placeholder class for basemaps
                {"display": "none"},
                {"display": "block"},
                {"display": "none"},  # Hides basemaps
                "tools",
            )

        elif trigger_id == "open-basemaps-link" and current_content != "basemaps":
            return (
                "slide-out",
                "slide-out",  # Add a default or placeholder class for charts
                "slide-in",  # Adds animation for basemaps
                {"display": "none"},
                {"display": "none"},
                {"display": "block"},  # Shows basemaps
                "basemaps",
            )

        return no_update, no_update, no_update, no_update, no_update, no_update, no_update

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
