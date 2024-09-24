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
    def handle_collapse_button_click(n_clicks):
        is_open = True if n_clicks % 2 == 1 else False
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

    # Navbar Button Click Callback
    @dashboard.callback(
        output={
            "charts_button_style": Output("charts-button", "style"),
            "tools_button_style": Output("tools-button", "style"),
            "buildings_button_style": Output("buildings-button", "style"),
            "clipboard_button_style": Output("clipboard-button", "style"),
            "layers_button_style": Output("layers-button", "style"),
            "list_button_style": Output("list-button", "style"),
            "basemaps-gallery_button_style": Output("basemaps-gallery-button", "style"),
            "charts_class_name": Output("charts", "className"),
            "tools_class_name": Output("arcgis-tools", "className"),
            "basemap_gallery_class_name": Output("basemap-gallery", "className"),
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
    def handle_navbar_button_click(*inputs):
        navbar_button_class_names = [
            "charts-button",
            "tools-button",
            "buildings-button",
            "clipboard-button",
            "layers-button",
            "list-button",
            "basemaps-gallery-button",
        ]

        # Get id of clicked button
        clicked_button_id = ctx.triggered_id if not None else ""

        active_button_style = {"background": "var(--main-color)", "color": "white"}
        active_drawer_class = "animate__animated animate__slideInUp"
        non_active_drawer_class = "hidden"

        def handle_navbar_button_style_update(button_id):
            if button_id == clicked_button_id:
                return active_button_style
            else:
                return {}

        # Update class of clicked button to slide-in animation
        def handle_drawer_class_name_update(button_id):
            if button_id == clicked_button_id:
                return active_drawer_class
            else:
                return non_active_drawer_class

        navbar_buttons_styles = list(
            map(
                handle_navbar_button_style_update,
                navbar_button_class_names,
            )
        )

        navbar_drawer_class_names = list(
            map(
                handle_drawer_class_name_update,
                navbar_button_class_names,
            )
        )

        # Default states when nothing has been clicked yet
        charts_button_style = (
            active_button_style
            if all(n_clicks == None for n_clicks in inputs)
            else navbar_buttons_styles[0]
        )

        charts_class_name = (
            active_drawer_class
            if all(n_clicks == None for n_clicks in inputs)
            else navbar_drawer_class_names[0]
        )

        return {
            "charts_button_style": charts_button_style,
            "tools_button_style": navbar_buttons_styles[1],
            "buildings_button_style": navbar_buttons_styles[2],
            "clipboard_button_style": navbar_buttons_styles[3],
            "layers_button_style": navbar_buttons_styles[4],
            "list_button_style": navbar_buttons_styles[5],
            "basemaps-gallery_button_style": navbar_buttons_styles[6],
            "charts_class_name": charts_class_name,
            "tools_class_name": navbar_drawer_class_names[1],
            "basemap_gallery_class_name": navbar_drawer_class_names[6],
        }
