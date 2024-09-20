import dash
from dash import Input, Output, State, no_update
import requests
import json
import random
from datetime import datetime, timedelta
def register_callbacks(dashboard):
    @dashboard.callback(
        Input("chart-data-store", "data"),
        prevent_initial_call=True
    )
    def print_data(data):
        print(f"printing from callback {data}")

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


    # Callback to fetch data and update the charts
    # @dashboard.callback(
    #     [
    #         Output("eff-yr-blt-chart", "data"),
    #         Output("tot-lvg-area-chart", "data"),
    #         Output("just-value-chart", "data"),
    #         Output("doruc-chart", "data"),
    #     ],
    #     [Input("event-listener-container", "n_events")],
    #     [State("event-listener-container", "event")],
    # )
    # def update_charts_from_event(event_count, event_data):
    #     print(f"Event count: {event_count},  Event data: {event_data}")
    #     if event_data:
    #         chart_data = event_data['detail']['chartData']
    #         return (
    #             chart_data['effyrblt_chart'],
    #             chart_data['totlvgarea_chart'],
    #             chart_data['jv_chart'],
    #             chart_data['doruc_chart']
    #         )
    #     return [], [], [], []

    # Populate Charts Callback  # Added to populate charts with random data
    @dashboard.callback(
        [
            Output("eff-yr-blt-chart", "data"),
            Output("tot-lvg-area-chart", "data"),
            Output("just-value-chart", "data"),
            Output("doruc-chart", "data"),
        ],
        [Input("populate-charts", "n_clicks")],
        prevent_initial_call=True,
    )
    def update_charts_from_btn(n_clicks):
        if n_clicks:
            # Simulate chart data by random generation
            test_data = {
                "totlvgarea_chart": [
                    {"TOTLVGAREA": random.randint(700, 5000)}
                    for _ in range(100)
                ],
                "jv_chart": [
                    {"value": random.randint(50000, 1500000)}  # Random just value data
                    for i in range(100)
                ],
                "doruc_chart": [
                    {"value": random.randint(10, 100)}  # Random value between 10 and 100 for DORUC
                    for _ in range(100)
                ]
            }

            # lists to hold categorized data
            years = list(range(1900, 2024))  # Years from 1900 to 2023

            # Generate random data for both EFFYRBLT and ACTYRBLT for each year
            effyrblt_data = [
                {"year": year, "effyrblt_count": random.randint(0, 20), "actyrblt_count": random.randint(0, 20)}
                for year in years
            ]

            # print(effyrblt_data)

            totlvgarea_data = []

            totlvgarea_category_counts = {
                "<1000": 0,
                "1000-2000": 0,
                "2000-3000": 0,
                ">3000": 0
            }

            jv_category_counts = {
                "<$100k": 0,
                "$100k-$500k": 0,
                "$500k-$1M": 0,
                ">$1M": 0
            }

            # Transform totlvgarea_chart data
            for entry in test_data["totlvgarea_chart"]:
                totlvgarea = entry["TOTLVGAREA"]
                if totlvgarea < 1000:
                    totlvgarea_category_counts["<1000"] += 1
                elif 1000 <= totlvgarea < 2000:
                    totlvgarea_category_counts["1000-2000"] += 1
                elif 2000 <= totlvgarea < 3000:
                    totlvgarea_category_counts["2000-3000"] += 1
                else:
                    totlvgarea_category_counts[">3000"] += 1

            # Convert totlvgarea_category_counts to the format required by the BarChart
            for category, count in totlvgarea_category_counts.items():
                totlvgarea_data.append({"category": category, category: count})

            # Transform jv_chart data into categorized ranges for the DonutChart
            for entry in test_data["jv_chart"]:
                jv_value = entry["value"]
                if jv_value < 100000:
                    jv_category_counts["<$100k"] += 1
                elif 100000 <= jv_value < 500000:
                    jv_category_counts["$100k-$500k"] += 1
                elif 500000 <= jv_value < 1000000:
                    jv_category_counts["$500k-$1M"] += 1
                else:
                    jv_category_counts[">$1M"] += 1

            # Convert jv_category_counts to the format required by the DonutChart with colors
            jv_data = [
                {"name": "<$100k", "value": jv_category_counts["<$100k"], "color": "indigo.6"},  # Violet
                {"name": "$100k-$500k", "value": jv_category_counts["$100k-$500k"], "color": "yellow.6"},  # Gold
                {"name": "$500k-$1M", "value": jv_category_counts["$500k-$1M"], "color": "teal.6"},
                # Lime Green
                {"name": ">$1M", "value": jv_category_counts[">$1M"], "color": "gray.6"}  # Tomato
            ]

            # Weight coefficients for each category for simulating DORUC data
            weights = {
                "Residential": 1.2,
                "Commercial": 1.0,
                "Industrial": 0.8,
                "Other": 0.2
            }

            # Categorize DORUC values into Residential, Commercial, Industrial, and Other
            doruc_category_counts = {
                "Residential": 0,
                "Commercial": 0,
                "Industrial": 0,
                "Other": 0
            }
            # Categorize DORUC values and accumulate the counts
            for entry in test_data["doruc_chart"]:
                doruc_value = entry["value"]

                # Categorize based on the DORUC value
                if 1 <= doruc_value <= 25:
                    doruc_category_counts["Residential"] += 1 * weights["Residential"]
                elif 26 <= doruc_value <= 50:
                    doruc_category_counts["Commercial"] += 1 * weights["Commercial"]
                elif 51 <= doruc_value <= 75:
                    doruc_category_counts["Industrial"] += 1 * weights["Industrial"]
                else:
                    doruc_category_counts["Other"] += 1 * weights["Other"]

            # Convert doruc_category_counts to the format required by the PieChart (only one entry per category)

            # color theme 1
            # doruc_data = [
            #     {"name": "Residential", "value": doruc_category_counts["Residential"], "color": "#5932EA"},
            #     {"name": "Commercial", "value": doruc_category_counts["Commercial"], "color": "#FFD700"},
            #     {"name": "Industrial", "value": doruc_category_counts["Industrial"], "color": "#32CD32"},
            #     {"name": "Other", "value": doruc_category_counts["Other"], "color": "#FF6347"}
            # ]

            # color theme 2
            doruc_data = [
                {"name": "Residential", "value": doruc_category_counts["Residential"], "color": "indigo.6"},
                {"name": "Commercial", "value": doruc_category_counts["Commercial"], "color": "yellow.6"},
                {"name": "Industrial", "value": doruc_category_counts["Industrial"], "color": "teal.6"},
                {"name": "Other", "value": doruc_category_counts["Other"], "color": "gray.6"}
            ]

            # Return the data to populate the charts
            return (effyrblt_data,
                    totlvgarea_data,
                    jv_data,
                    doruc_data)

        return [], [], [], []

