from dash import Input, Output, State, no_update, ctx


def register_callbacks(dashboard):
    # Collapse Sidebar Callback
    @dashboard.callback(
        prevent_initial_call=True,
        output={
            "navbar_drawer_className": Output("navbar-drawer", "className"),
            "collapse_icon": Output("collapse-icon", "icon"),
        },
        inputs=[
            Input("collapse-button", "n_clicks"),
        ],
    )
    def toggle_drawer_and_size(n_clicks):
        is_open = True if n_clicks % 2 == 0 else False
        new_icon = (
            "heroicons:chevron-double-right-16-solid"
            if is_open
            else "heroicons:chevron-double-left-16-solid"
        )
        className = (
            "animate__animated animate__slideOutLeft"
            if is_open
            else "animate__animated animate__slideInLeft"
        )
        return {"navbar_drawer_className": className, "collapse_icon": new_icon}

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
            "charts_class_name": Output("charts", "className"),
            "tools_className": Output("arcgis-tools", "className"),
            "basemap_gallery_className": Output("basemap-gallery", "className"),
        },
        inputs=[
            Input("charts-button", "n_clicks"),
            Input("tools-button", "n_clicks"),
            Input("buildings-button", "n_clicks"),
            Input("clipboard-button", "n_clicks"),
            Input("layers-button", "n_clicks"),
            Input("list-button", "n_clicks"),
            Input("basemaps-gallery-button", "n_clicks"),
        ],
    )
    def handle_sidebar_icon_click(*inputs):
        # Get id of clicked button
        clicked_button_id = ctx.triggered_id if not None else ""

        # Update class of clicked button to slide-in animation
        def handle_button_click(button_id):
            if button_id == clicked_button_id:
                return f"slide-in"
            else:
                return f"hidden"

        outputs = map(
            handle_button_click,
            [
                "charts-button",
                "tools-button",
                "buildings-button",
                "clipboard-button",
                "layers-button",
                "list-button",
                "basemaps-gallery-button",
            ],
        )
        outputs = list(outputs)

        charts_class_name = (
            "slide-in" if all(n_clicks == None for n_clicks in inputs) else outputs[0]
        )

        return {
            "charts_class_name": charts_class_name,
            "tools_className": outputs[1],
            "basemap_gallery_className": outputs[6],
        }
