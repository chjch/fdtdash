from dash import Input, Output, State, no_update, ctx


def register_callbacks(dashboard):
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
            'charts_class_name': Output('chart_scrollable_div', 'className'),
            'tools_className':  Output('arcgistools_scrollable_div', 'className'),
            'basemap_gallery_className': Output('basemap-gallery-container', 'className'),
            },     
        inputs=[
            Input('charts-toggle-button', 'n_clicks'),
            Input('arcgis-tools-toggle-button', 'n_clicks'),
            Input('buildings-toggle-button', 'n_clicks'),
            Input('clipboard-toggle-button', 'n_clicks'),
            Input('layers-toggle-button', 'n_clicks'),
            Input('list-toggle-button', 'n_clicks'),
            Input('maps-toggle-button', 'n_clicks')])
    def handle_sidebar_icon_click(*inputs):
        button_id = ctx.triggered_id if not None else ''
        
        def handle_button_click(button_class_name):
            if button_class_name == button_id:
                return f'{button_class_name} slide-in'
            else:
                return 'hidden'

        outputs = map(handle_button_click, 
                    ['charts-toggle-button',
                    'arcgis-tools-toggle-button', 
                    'buildings-toggle-button',
                    'clipboard-toggle-button',
                    'layers-toggle-button',
                    'list-toggle-button',
                    'maps-toggle-button'])
        outputs = list(outputs)

        charts_class_name = 'charts-toggle-button slide-in' if all(clicks == None for clicks in inputs) else outputs[0]

        return {
            'charts_class_name': charts_class_name,
            'tools_className': outputs[1],
            'basemap_gallery_className': outputs[6],
        }