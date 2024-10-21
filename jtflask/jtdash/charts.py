from dash import html
import dash_mantine_components as dmc


# Function to create charts
def get_charts():
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
                    id="yearSelectValue", size="lg", className="yearSelectText"
                ),
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
                dmc.Text(
                    id="stormSelectValue",
                    size="lg",
                    className="stormSelectText",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="Scenario_card",
            className="cardChart",
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
                    series=[
                        {
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
                    withTooltip=False,
                    tickLine="xy",
                    gridAxis="xy",
                    barChartProps={"barSize": 50},
                    id="tot-lvg-area-chart",
                    style={"margin": "10px", "backgroundColor": "#f4f4f9"},
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
        id="charts",
        className="mantine-Drawer-body-item",
    )
