from dash import Input, Output, ctx, clientside_callback, ClientsideFunction


def register_callbacks(dashboard):
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


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="handleNavbarButtonClick"),
    # Dummy Output. Not used. Not needed in newer versions of dash
    Output("navbar-control", "className"),
    # Inputs
    Input("charts-button", "n_clicks"),
    Input("tools-button", "n_clicks"),
    Input("basemaps-gallery-button", "n_clicks"),
    Input("collapse-button", "n_clicks"),
)
