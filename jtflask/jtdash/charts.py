import dash_mantine_components as dmc
from dash import html, dcc
import json
import os

# # Function to load data from JSON files in the assets folder APP  reference
# def load_data_from_assets(file_path):
#     with open(file_path, 'r') as file:
#         return json.load(file)
#
# # Load data from JSON files
# def get_data(app):
#     assets_folder = app.config.assets_folder
#     data = load_data_from_assets(os.path.join(assets_folder, 'data', 'data.json'))
#     data2 = load_data_from_assets(os.path.join(assets_folder, 'data', 'data2.json'))
#     data3 = load_data_from_assets(os.path.join(assets_folder, 'data', 'data3.json'))
#     return data, data2, data3


# Define the relative path to the assets folder
ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "assets")


# Function to load data from JSON files in the assets folder
def load_data_from_assets(file_name):
    file_path = os.path.join(ASSETS_FOLDER, "data", file_name)
    with open(file_path, "r") as file:
        return json.load(file)


# Load data from JSON files
def get_data():
    data = load_data_from_assets("data.json")
    data2 = load_data_from_assets("data2.json")
    data3 = load_data_from_assets("data3.json")
    return data, data2, data3


# Function to create charts
def create_charts():
    # assets_folder = app.config.assets_folder
    data, data2, data3 = get_data()
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
            id="Scenario_card",
            className="cardChart",
        ),
        dmc.Card(
            children=[
                dmc.Text("Area Chart", size="lg", className="chartLabel"),
                dmc.AreaChart(
                    h=200,
                    dataKey="date",
                    data=data,
                    series=[
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"},
                    ],
                    curveType="linear",
                    tickLine="xy",
                    withGradient=False,
                    withXAxis=False,
                    withDots=False,
                    id="area_chart",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="Areachart_card",
            className="cardChart",
        ),
        dmc.Card(
            children=[
                dmc.Text("Bar Chart", size="lg", className="chartLabel"),
                dmc.BarChart(
                    h=200,
                    dataKey="month",
                    data=data3,
                    type="percent",
                    series=[
                        {"name": "Smartphones", "color": "violet.6"},
                        {"name": "Laptops", "color": "blue.6"},
                        {"name": "Tablets", "color": "teal.6"},
                    ],
                    id="barchart_bar",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="barchart_card",
            className="cardChart",
        ),
        dmc.Card(
            children=[
                dmc.Text("Donut Chart", size="lg", className="chartLabel"),
                dmc.DonutChart(
                    data=data2, withLabels=True, withLabelsLine=True, id="donut_chart"
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="donut_card",
            className="cardChart",
        ),
        dmc.Card(
            children=[
                dmc.Text("Line Chart", size="lg", className="chartLabel"),
                dmc.LineChart(
                    h=200,
                    dataKey="date",
                    data=data,
                    series=[
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"},
                    ],
                    curveType="linear",
                    tickLine="xy",
                    withXAxis=False,
                    withDots=False,
                    id="line_chart",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="line_card",
            className="cardChart",
        ),
        dmc.Card(
            children=[
                dmc.Text("Pie Chart", size="lg", className="chartLabel"),
                dmc.PieChart(
                    data=data2,
                    withLabelsLine=True,
                    labelsPosition="inside",
                    labelsType="percent",
                    withLabels=True,
                    id="pie_chart",
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            id="pie_card",
            className="cardChart",
        ),
    ]
    
    #
    return html.Div(
        id="charts", children=charts, 
    )
