from collections import defaultdict
from dash import Input, Output, State, no_update, ctx


def register_callbacks(dashboard):
    # update data store callback with selected data
    @dashboard.callback(
        [
            Output("eff-yr-blt-chart", "data"),
            Output("tot-lvg-area-chart", "data"),
            Output("just-value-chart", "data"),
            Output("doruc-chart", "data"),
        ],
        [Input("chart-data-store", "data")],
        prevent_initial_call=True,
    )
    def update_data_store(data):
        if not data:
            return [], [], [], []  # Return empty data if no data is received

        # Initialize data structures for processing
        effyrblt_counts = defaultdict(
            int
        )  # To hold count of EFFYRBLT per year
        totlvgarea_category_counts = {
            "NA": 0,
            "<1000": 0,
            "1000-2000": 0,
            "2000-3000": 0,
            ">3000": 0,
        }
        jv_category_counts = {
            "NA": 0,
            "<$100k": 0,
            "$100k-$500k": 0,
            "$500k-$1M": 0,
            ">$1M": 0,
        }
        doruc_category_counts = {
            "NA": 0,
            "Residential": 0,
            "Commercial": 0,
            "Industrial": 0,
            "Other": 0,
        }

        # Process each entry from the received data
        for entry in data:
            # Process Effective Year Built (EFFYRBLT)
            effyrblt_year = entry.get("EFFYRBLT")
            if effyrblt_year is not None:
                effyrblt_counts[
                    effyrblt_year
                ] += 1  # Count occurrences per year

            # Process Total Living Area (TOTLVGAREA)
            totlvgarea = entry.get("TOTLVGAREA", 0)

            # Check if the value is None or zero and categorize as "NA"
            if totlvgarea is None or totlvgarea == 0:
                totlvgarea_category_counts["NA"] += 1
            elif totlvgarea < 1000:
                totlvgarea_category_counts["<1000"] += 1
            elif 1000 <= totlvgarea < 2000:
                totlvgarea_category_counts["1000-2000"] += 1
            elif 2000 <= totlvgarea < 3000:
                totlvgarea_category_counts["2000-3000"] += 1
            else:
                totlvgarea_category_counts[">3000"] += 1

            # Process Just Value (JV)
            jv_value = entry.get("JV", 0)

            if jv_value is None or jv_value == 0:
                jv_category_counts["NA"] += 1
            elif jv_value < 100000:
                jv_category_counts["<$100k"] += 1
            elif 100000 <= jv_value < 500000:
                jv_category_counts["$100k-$500k"] += 1
            elif 500000 <= jv_value < 1000000:
                jv_category_counts["$500k-$1M"] += 1
            else:
                jv_category_counts[">$1M"] += 1

            # Process DORUC
            doruc_value = entry.get("DORUC", "")
            if doruc_value is None or doruc_value == 0:
                doruc_category_counts["NA"] += 1
            elif 1 <= int(doruc_value) <= 25:
                doruc_category_counts["Residential"] += 1
            elif 26 <= int(doruc_value) <= 50:
                doruc_category_counts["Commercial"] += 1
            elif 51 <= int(doruc_value) <= 75:
                doruc_category_counts["Industrial"] += 1
            else:
                doruc_category_counts["Other"] += 1

        # Format EFFYRBLT data to match the required format
        effyrblt_data = [
            {"year": year, "effyrblt_count": count}
            for year, count in sorted(effyrblt_counts.items())
        ]

        # Convert totlvgarea_category_counts to the format required by the BarChart
        totlvgarea_data = [
            {"category": category, category: count}
            for category, count in totlvgarea_category_counts.items()
        ]

        # Convert jv_category_counts to the format required by the DonutChart with colors
        jv_data = [
            {
                "name": "NA",
                "value": jv_category_counts["NA"],
                "color": "gray.6",
            },
            {
                "name": "<$100k",
                "value": jv_category_counts["<$100k"],
                "color": "indigo.6",
            },
            {
                "name": "$100k-$500k",
                "value": jv_category_counts["$100k-$500k"],
                "color": "yellow.6",
            },
            {
                "name": "$500k-$1M",
                "value": jv_category_counts["$500k-$1M"],
                "color": "teal.6",
            },
            {
                "name": ">$1M",
                "value": jv_category_counts[">$1M"],
                "color": "violet.6",
            },
        ]

        # Convert doruc_category_counts to the format required by the PieChart
        doruc_data = [
            {
                "name": "NA",
                "value": doruc_category_counts["NA"],
                "color": "gray.6",
            },
            {
                "name": "Residential",
                "value": doruc_category_counts["Residential"],
                "color": "indigo.6",
            },
            {
                "name": "Commercial",
                "value": doruc_category_counts["Commercial"],
                "color": "yellow.6",
            },
            {
                "name": "Industrial",
                "value": doruc_category_counts["Industrial"],
                "color": "teal.6",
            },
            {
                "name": "Other",
                "value": doruc_category_counts["Other"],
                "color": "violet.6",
            },
        ]
        return effyrblt_data, totlvgarea_data, jv_data, doruc_data

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
    def toggle_sidebar_drawer(n_clicks, is_open):
        new_icon = (
            "heroicons:chevron-double-right-16-solid"
            if is_open
            else "heroicons:chevron-double-left-16-solid"
        )
        return not is_open, new_icon

    # Sidebar Button Click Callback
    @dashboard.callback(
        output={
            "charts_class_name": Output("chart_scrollable_div", "className"),
            "tools_className": Output(
                "arcgistools_scrollable_div", "className"
            ),
            "scrollable_div_bulding_className": Output("scrollable_div_bulding_stats", "className"),
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
                return f"{button_id} mantine-Drawer-body-item slide-in"
            else:
                return f"{button_id} mantine-Drawer-body-item hidden "

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
            "charts-toggle-button mantine-Drawer-body-item slide-in"
            if all(n_clicks is None for n_clicks in inputs)
            else outputs[0]
        )

        return {
            "charts_class_name": charts_class_name,
            "tools_className": outputs[1],
            "scrollable_div_bulding_className": outputs[2],
            "basemap_gallery_className": outputs[6],
        }

    # Scenario Chart callback
    @dashboard.callback(
        Output("yearSelectValue", "children"),
        Input("yearSelect", "value")
    )
    def select_value(value):
        return value

    @dashboard.callback(
        Output("stormSelectValue", "children"),
        Input("stormSelect", "value")
    )
    def select_value(value):
        return value
