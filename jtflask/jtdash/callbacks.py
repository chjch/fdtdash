import dash
from dash import Input, Output, State, no_update


def register_callbacks(dashboard):
    @dashboard.callback(
        [
            Output("chart_scrollable_div", "className"),
            Output("arcgistools_scrollable_div", "className"),
            Output("chart_scrollable_div", "style"),
            Output("arcgistools_scrollable_div", "style"),
            Output("drawer-content-store", "data"),
        ],
        [
            Input("open-charts-drawer-link", "n_clicks"),
            Input("open-arcgis-drawer-link", "n_clicks"),
        ],
        [State("drawer-content-store", "data")],
        prevent_initial_call=True,
    )
    def update_drawer_content(charts_click, tools_click, current_content):
        ctx = dash.callback_context

        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        # List of sidebar icon NavLinks that should trigger the callback
        valid_navlinks = ["open-charts-drawer-link", "open-arcgis-drawer-link"]

        # Only execute if the trigger is a sidebar icon NavLink
        if trigger_id not in valid_navlinks:
            return no_update, no_update, no_update, no_update, no_update

        if (
            trigger_id == "open-charts-drawer-link"
            and current_content != "charts"
        ):
            return (
                "slide-in",
                "slide-out",
                {"display": "block"},
                {"display": "none"},
                "charts",
            )

        elif (
            trigger_id == "open-arcgis-drawer-link"
            and current_content != "tools"
        ):
            return (
                "slide-out",
                "slide-in",
                {"display": "none"},
                {"display": "block"},
                "tools",
            )

        return no_update, no_update, no_update, no_update, no_update

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
