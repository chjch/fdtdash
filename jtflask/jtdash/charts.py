import dash_mantine_components as dmc
from dash import html
import json
import os

# Define the relative path to the assets folder
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'assets')

# Function to load data from JSON files in the assets folder

# Function to create charts
def create_charts():

    charts = [
        dmc.Card(
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
                dmc.Text(id="yearSelectValue", size="lg", className="yearSelectText"),
                dmc.Select(
                    comboboxProps={"position": "bottom"},
                    placeholder="Storm",
                    id="stormSelect",
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
                dmc.Text(id="stormSelectValue", size="lg", className="stormSelectText"),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="Scenario_card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.Text("Land Use (DORUC)", size="lg", className="chartLabel"),
                dmc.PieChart(
                    h=300,
                    data=[
                        {"name": "Residential", "value": 40, "color": "green.6"},
                        {"name": "Commercial", "value": 30, "color": "blue.6"},
                        {"name": "Industrial", "value": 20, "color": "purple.6"},
                        {"name": "Other", "value": 10, "color": "red.6"}
                    ],
                    withLabelsLine=True,
                    withTooltip=True,
                    tooltipDataSource="segment",
                    labelsPosition="outside",
                    labelsType="percent",
                    withLabels=True,
                    strokeColor="white",
                    id="doruc-chart",
                    size="220",
                    style={
                        "margin": "10px",
                        "backgroundColor": "#f9f9f9"
                    }
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="doruc-card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.Text("Just Value (JV)", size="lg", className="chartLabel"),
                dmc.DonutChart(
                    chartLabel="Just Value (JV)",
                    h=300,
                    data=[
                        {"name": "<$100k", "value": 15, "color": "red"},
                        {"name": "$100k-$500k", "value": 45, "color": "green"},
                        {"name": "$500k-$1M", "value": 25, "color": "blue"},
                        {"name": ">$1M", "value": 10, "color": "orange"}
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
                    style={
                        "margin": "10px",
                        "backgroundColor": "#f4f4f9"
                    }
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="just-value-card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.Text("Effective Year Built / Actual Year Built", size="lg", className="chartLabel"),

                dmc.AreaChart(
                    h=300,
                    dataKey="year",
                    data=[],

                    series=[ {
                                "name": "effyrblt_count",
                                "dataKey": "effyrblt_count",
                                "color": "indigo.6"
                            },
                            {
                                "name": "actyrblt_count",
                                "dataKey": "actyrblt_count",
                                "color": "teal.6"
                            }],
                    curveType="bump",
                    tickLine="xy",
                    withGradient=False,
                    withXAxis=True,
                    withYAxis=True,
                    withDots=False,
                    yAxisProps={'domain': [0, 25]},
                    id="eff-yr-blt-chart"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="eff-yr-blt-card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.Text("Total Living Area (square feet) ", size="lg", className="chartLabel"),
                dmc.BarChart(
                    h=300,
                    dataKey="category",
                    data=[
                        {"category": "<1000 sq ft", "value": 10},
                        {"category": "1000-2000 sq ft", "value": 25},
                        {"category": "2000-3000 sq ft", "value": 35},
                        {"category": ">3000 sq ft", "value": 20}
                    ],
                    type="vertical",
                    series=[
                        {"name": "<1000",  "color": "violet.6"},
                        {"name": "1000-2000",   "color": "blue.6"},
                        {"name": "2000-3000",  "color": "teal.6"},
                        {"name": ">3000",  "color": "yellow.6"}
                    ],
                    withXAxis=True,
                    withYAxis=True,
                    withTooltip=False,
                    tickLine="xy",
                    gridAxis="xy",
                    # yAxisProps={"width": 80},
                    # xAxisProps={"width": 80},
                    barChartProps={"barSize": 50},
                    id="tot-lvg-area-chart",
                    style={ "margin": "10px", "backgroundColor": "#f4f4f9" },
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="tot-lvg-area-card",
            className="cardChart"
        ),

    ]
    return charts
