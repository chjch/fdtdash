from dash import html
import dash_mantine_components as dmc
from .utils import get_icon


# Function to create charts
def create_charts():
    charts = [
        dmc.Card(  # scenario card: id="Scenario_card", className="cardChart"
            children=[
                dmc.Text("Hazard", size="lg", className="chartLabel"),
                dmc.Select(
                    comboboxProps={"position": "bottom"},
                    placeholder="Year",
                    id="yearSelect",
                    value="2040",
                    data=[
                        {"value": "2040", "label": "Year"},
                        {"value": "2060", "label": "Year"},
                        {"value": "2080", "label": "Year"},
                        {"value": "2100", "label": "Year"},
                    ],
                    w=100,
                    mb=10,
                ),
                dmc.Text(
                    id="year-select-value", size="lg", className="year-select-text"
                ),
                dmc.Select(
                    comboboxProps={"position": "bottom"},
                    placeholder="Storm",
                    id="storm-select",
                    value="Category-1 Hurricane",
                    data=[
                        {"value": "Category-1 Hurricane", "label": "Storm"},
                        {"value": "Category-2 Hurricane", "label": "Storm"},
                        {"value": "Category-3 Hurricane", "label": "Storm"},
                        {"value": "Category-4 Hurricane", "label": "Storm"},
                    ],
                    w=100,
                    mb=10,
                ),
                dmc.Text(
                    id="storm-select-value",
                    size="lg",
                    className="storm-select-text",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="Scenario_card",
            className="cardChart hidden",
        ),
        dmc.Card(
            children=[
                # Dock/Undock button
                dmc.Button([get_icon("solar:maximize-square-3-outline", "dock-icon")],
                           id="undock-button",
                           className="undock-button",
                           variant="subtle",
                           color="gray",
                           style={"position": "absolute",
                                  "marginBottom": "2px",
                                  "top": "0px",
                                  "right": "-5px",
                                  "size": "sm",}),
                dmc.Text("Building Statistics", size="lg", className="chartLabel building-stats-card-label"),

                # Display building count
                dmc.Group(
                    children=[
                        dmc.Text("Total Buildings: ", id="building-selection-count-label", size="md"),
                        dmc.Text(id="building-selection-count-value", size="md"),  # To be updated dynamically
                    ],
                    # position="apart",
                    style={"marginBottom": "15px"}
                ),

                # Tabbed interface for each category
                dmc.Tabs(
                    children=[
                        dmc.TabsList(
                            children=[
                                dmc.TabsTab("Residential", value="residential"),
                                dmc.TabsTab("Commercial", value="commercial"),
                                dmc.TabsTab("Industrial", value="industrial"),
                                dmc.TabsTab("Other", value="other"),
                            ]
                        ),
                        dmc.TabsPanel(
                            children=[
                                dmc.Text("Residential", size="md"),
                                dmc.List(
                                    children=[
                                        dmc.ListItem("Residential buildings are mainly used for housing."),
                                        dmc.ListItem("Typical features: single-family homes, apartments, etc."),
                                        dmc.ListItem("This category includes all buildings used for living purposes."),
                                    ],
                                    style={"marginTop": "10px"}
                                )
                            ],
                            value="residential",
                        ),
                        dmc.TabsPanel(
                            children=[
                                dmc.Text("Commercial", size="md"),
                                dmc.List(
                                    children=[
                                        dmc.ListItem("Commercial buildings are used for business purposes."),
                                        dmc.ListItem("Typical features: offices, retail stores, hotels, etc."),
                                        dmc.ListItem(
                                            "This category includes all buildings used for commercial activities."),
                                    ],
                                    style={"marginTop": "10px"}
                                )
                            ],
                            value="commercial",
                        ),
                        dmc.TabsPanel(
                            children=[
                                dmc.Text("Industrial", size="md"),
                                dmc.List(
                                    children=[
                                        dmc.ListItem("Industrial buildings are used for manufacturing or production."),
                                        dmc.ListItem("Typical features: factories, warehouses, etc."),
                                        dmc.ListItem(
                                            "This category includes all buildings used for industrial purposes."),
                                    ],
                                    style={"marginTop": "10px"}
                                )
                            ],
                            value="industrial",
                        ),
                        dmc.TabsPanel(
                            children=[
                                dmc.Text("Other", size="md"),
                                dmc.List(
                                    children=[
                                        dmc.ListItem(
                                            "This category includes buildings that do not fall under other types."),
                                        dmc.ListItem("Examples: public spaces, entertainment venues, etc."),
                                    ],
                                    style={"marginTop": "10px"}
                                )
                            ],
                            value="other",
                        )
                    ],
                    style={"marginTop": "15px"},
                    orientation="horizontal",
                    # grow=True,  # Expand the tab content to fit
                    value="residential"  # Default active tab
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="building-selection-stats-card",
            className="cardChart"
        ),
        dmc.Card(  # doruc card: id="doruc-card", className="cardChart"
            children=[
                dmc.Text(
                    "Land Use (DORUC)", size="lg", className="chartLabel"
                ),
                dmc.PieChart(
                    h=300,
                    data=[
                        {"name": "NA", "value": 40, "color": "gray.6"},
                        {
                            "name": "Residential",
                            "value": 40,
                            "color": "violet.6",
                        },
                        {"name": "Commercial", "value": 30, "color": "blue.6"},
                        {"name": "Industrial", "value": 20, "color": "teal.6"},
                        {"name": "Other", "value": 10, "color": "yellow.6"},
                    ],

                    withLabelsLine=True,
                    withTooltip=True,
                    tooltipDataSource="segment",
                    tooltipProps={
                        "style": {
                            "backgroundColor": "white",
                            "color": "blacks",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "fontSize": "18px",
                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.3)"
                        }
                    },
                    labelsPosition="outside",
                    labelsType="percent",
                    withLabels=True,

                    strokeColor="white",
                    id="doruc-chart",
                    size="220",
                    style={"margin": "10px", "backgroundColor": "#f9f9f9"},
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="doruc-card",
            className="cardChart",
        ),
        dmc.Card(  # jv_card: id="just-value-card", className="cardChart"
            children=[
                dmc.Text("Just Value (JV)", size="lg", className="chartLabel"),
                dmc.DonutChart(
                    chartLabel="Just Value (JV)",
                    h=300,
                    data=[
                        {"name": "NA", "value": 15, "color": "gray.6"},
                        {"name": "<$100k", "value": 15, "color": "violet.6"},
                        {
                            "name": "$100k-$500k",
                            "value": 45,
                            "color": "violet.6",
                        },
                        {"name": "$500k-$1M", "value": 25, "color": "teal.6"},
                        {"name": ">$1M", "value": 10, "color": "yellow.6"},
                    ],
                    withLabels=True,
                    # withLabelsLine=True,
                    withTooltip=True,
                    tooltipDataSource="segment",

                    strokeColor="white",
                    strokeWidth=1,
                    size="220",
                    id="just-value-chart",
                    labelColor="black",
                    thickness="30",
                    style={"backgroundColor": "#f4f4f9"},
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="just-value-card",
            className="cardChart",
        ),
        dmc.Card(  # eff-yr card: id="eff-yr-blt-card", className="cardChart"
            children=[
                # dmc.Text("Effective Year Built / Actual Year Built", size="lg", className="chartLabel"),
                dmc.Text(
                    "Effective Year Built", size="lg", className="chartLabel"
                ),
                dmc.AreaChart(
                    h=300,
                    dataKey="year",
                    data=[],
                    withLegend=False,
                    legendProps={"verticalAlign": "bottom", "height": 50},
                    series=[
                        {
                            "label": "Effective Year Built",
                            "name": "effyrblt_count",
                            "dataKey": "effyrblt_count",
                            "color": "indigo.6",
                        },
                        {
                            "name": "actyrblt_count",
                            "dataKey": "actyrblt_count",
                            "color": "teal.6",
                        },
                    ],
                    curveType="bump",
                    tickLine="xy",
                    withGradient=False,
                    withXAxis=True,
                    withYAxis=True,
                    withDots=False,
                    yAxisProps={"domain": [0, 25]},
                    id="eff-yr-blt-chart",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="eff-yr-blt-card",
            className="cardChart",
        ),
        dmc.Card(  # tot-lvg card: id="tot-lvg-area-card", className="cardChart"
            children=[
                dmc.Text(
                    "Total Living Area (square feet) ",
                    size="lg",
                    className="chartLabel",
                ),
                dmc.BarChart(
                    h=300,
                    dataKey="category",
                    data=[
                        {"category": "NA", "NA": 20},
                        {"category": "<1000", "<1000": 10},
                        {"category": "1000-2000", "1000-2000": 25},
                        {"category": "2000-3000", "2000-3000": 35},
                        {"category": ">3000", ">3000": 20},
                    ],
                    series=[
                        {"name": "NA", "label": "N/A", "color": "gray.6"},
                        {
                            "name": "<1000",
                            "label": "<1000 sqft",
                            "color": "violet.6",
                        },
                        {
                            "name": "1000-2000",
                            "label": "<1000-2000 sqft",
                            "color": "blue.6",
                        },
                        {
                            "name": "2000-3000",
                            "label": "2000-3000 sqft",
                            "color": "teal.6",
                        },
                        {
                            "name": ">3000",
                            "label": ">3000 sqft",
                            "color": "yellow.6",
                        },
                    ],
                    withXAxis=True,
                    withYAxis=True,
                    withTooltip=True,
                    tooltipProps={
                        "style": {
                            "backgroundColor": "white",
                            "color": "white",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "fontSize": "14px",
                            "boxShadow": "0px 4px 8px rgba(0, 0, 0, 0.3)"
                        }
                    },
                    tickLine="x",
                    gridAxis="x",
                    withLegend=False,
                    barChartProps={"barSize": 100},
                    id="tot-lvg-area-chart",
                    style={"margin": "10px", "backgroundColor": "green.1"},
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="tot-lvg-area-card",
            className="cardChart",
        ),
    ]

    return html.Div(
        children=charts,
        id="chart_scrollable_div",
        className="mantine-Drawer-body-item",
    )
