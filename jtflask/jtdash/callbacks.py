from dash import Input, Output, State, no_update, ctx


def register_callbacks(dashboard):
    @dashboard.callback(
        Input("chart-data-store", "data"), prevent_initial_call=True
    )
    def print_data(data):
        print(f"printing from callback {data}")

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

    # Sidebar Button Click Callback
    @dashboard.callback(
        output={
            "charts_class_name": Output("chart_scrollable_div", "className"),
            "tools_className": Output(
                "arcgistools_scrollable_div", "className"
            ),
            "basemap_gallery_className": Output(
                "drawer-basemap-gallery", "className"
            ),
        },
        inputs=[
            Input("charts-toggle-button", "n_clicks"),
            Input("arcgis-tools-toggle-button", "n_clicks"),
            Input("buildings-toggle-button", "n_clicks"),
            Input("clipboard-toggle-button", "n_clicks"),
            Input("layers-toggle-button", "n_clicks"),
            Input("legend-toggle-button", "n_clicks"),
            Input("basemap-gallery-toggle-button", "n_clicks"),
        ],
    )
    def handle_sidebar_icon_click(*inputs):
        # Get id of clicked button
        clicked_button_id = ctx.triggered_id if not None else ""

        # Update class of clicked button to slide-in animation
        def handle_button_click(button_id):
            if button_id == clicked_button_id:
                return f"{button_id} slide-in"
            else:
                return f"{button_id} hidden"

        outputs = map(
            handle_button_click,
            [
                "charts-toggle-button",
                "arcgis-tools-toggle-button",
                "buildings-toggle-button",
                "clipboard-toggle-button",
                "layers-toggle-button",
                "legend-toggle-button",
                "basemap-gallery-toggle-button",
            ],
        )
        outputs = list(outputs)

        charts_class_name = (
            "charts-toggle-button slide-in"
            if all(n_clicks is None for n_clicks in inputs)
            else outputs[0]
        )

        return {
            "charts_class_name": charts_class_name,
            "tools_className": outputs[1],
            "basemap_gallery_className": outputs[6],
        }
