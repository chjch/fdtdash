from collections import defaultdict
from dash import Input, Output, State, no_update, ctx
import json


def register_callbacks(dashboard):
    # update data store callback with selected data
    @dashboard.callback(
        [
            Output("eff-yr-blt-chart", "data"),
            Output("tot-lvg-area-chart", "data"),
            Output("just-value-chart", "data"),
            Output("doruc-chart", "data"),
            Output("building-selection-count-value", "children")
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

        total_buildings = 0

        # Process each entry from the received data
        for entry in data:
            total_buildings += 1
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
        return effyrblt_data, totlvgarea_data, jv_data, doruc_data, str(total_buildings)

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
            "tools_className": Output("arcgistools_scrollable_div", "className"),
            "scrollable_div_building_className": Output("scrollable_div_building_stats",
                                                       "className"),
            "basemap_gallery_className": Output("drawer-basemap-gallery", "className"),
            "scrollable_div_layer_tools": Output("scrollable_div_layer_tools", "className"),
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
            "scrollable_div_building_className": outputs[2],
            "scrollable_div_layer_tools": outputs[4],
            "basemap_gallery_className": outputs[6],
        }

    # Scenario Chart callback
    @dashboard.callback(
        Output("year-select-value", "children"),
        Input("yearSelect", "value")
    )
    def select_value(value):
        return value

    @dashboard.callback(
        Output("storm-select-value", "children"),
        Input("storm-select", "value")
    )
    def select_value(value):
        return value

    # Dash callback to handle changes in RadioGroup and send to dashToMap
    @dashboard.callback(
        Output("map-action-store", "data",allow_duplicate=True),
        Input("colorMixModeRadioGroup", "value"),
        prevent_initial_call=True,
    )
    def update_texture_mode(selected_mode):
        # Prepare the data to send to JavaScript
        return {
            "action": "updateLayerTexture",
            "payload": {
                "mode": selected_mode
            }
        }

    # Assuming the extents dictionary is available here or imported if necessary
    neighborhoods = {
        "Downtown": {"xmin": -81.663, "ymin": 30.321, "xmax": -81.640, "ymax": 30.340},
        "Riverside": {"xmin": -81.693, "ymin": 30.304, "xmax": -81.670, "ymax": 30.320},
        "San Marco": {"xmin": -81.667, "ymin": 30.290, "xmax": -81.645, "ymax": 30.310},
        # Add more neighborhoods with their extents as needed
    }

    @dashboard.callback(
        Output("map-action-store", "data",allow_duplicate=True),
        Input("neighborhood-dropdown", "value"),
        prevent_initial_call=True,
    )
    def update_extent_store(selected_neighborhood):
        if selected_neighborhood in neighborhoods:
            extent = neighborhoods[selected_neighborhood]
            return {
                "action": "zoomToExtent",
                "payload": {
                    "extent_payload": {
                        "xmin": extent["xmin"],
                        "ymin": extent["ymin"],
                        "xmax": extent["xmax"],
                        "ymax": extent["ymax"]
                    }
                }
        }
        return None


    # Define the callback to trigger `initMap` based on radio group selection
    @dashboard.callback(
        Output("map-action-store", "data", allow_duplicate=True),
        Input("sceneLayerRadioGroup", "value"),
        prevent_initial_call=True,
    )
    def update_map_layer(selected_layer, zoom_to_full_extent=True):

        # URLs for each scene layer
        layer_urls = {
            "Downtown_Saint_Jones_River_SceneServer": "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Downtown_Saint_Jones_River/SceneServer",
            "Ribault_2_SceneServer": "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Ribault_2/SceneServer",
            "Ribault_Scenic_Drive_Park_SceneServer": "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Ribault_Scenic_Drive_Park/SceneServer",
            "Hogen_Creek_Neighborhood_SceneServer": "https://services.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/PLW_Jacksonville_BLD_Hogen_Creek_Neighborhood/SceneServer",
            "demImageServer": "https://tiledimageservices.arcgis.com/LBbVDC0hKPAnLRpO/arcgis/rest/services/USGS_1M_DEM_50M_Resample/ImageServer"
        }

        # Fetch the layer URL based on selection
        layer_url = layer_urls.get(selected_layer)

        # Return action and payload for `initMap`
        return {
            "action": "initMap",
            "payload": {
                "mapContainerId": "digital-twin-container",
                "layerUrl": layer_url,
                "zoomToFullExtent": zoom_to_full_extent
            }
        }