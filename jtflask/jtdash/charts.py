import dash_mantine_components as dmc
from dash import html, dcc
import json
import os

# Function to load data from JSON files in the assets folder
def load_data_from_assets(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load data from JSON files
def get_data(app):
    assets_folder = app.config.assets_folder
    data = load_data_from_assets(os.path.join(assets_folder, 'data', 'data.json'))
    data2 = load_data_from_assets(os.path.join(assets_folder, 'data', 'data2.json'))
    data3 = load_data_from_assets(os.path.join(assets_folder, 'data', 'data3.json'))
    return data, data2, data3

# Function to create charts
def create_charts(app):
    assets_folder = app.config.assets_folder
    data, data2, data3 = get_data(app)
    charts = [
        dmc.Card(
            children=[
                dmc.AreaChart(
                    h=200,
                    dataKey="date",
                    data=data,
                    series=[
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"}
                    ],
                    curveType="linear",
                    tickLine="xy",
                    withGradient=False,
                    withXAxis=False,
                    withDots=False,
                    id="area_chart"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="Areachart_card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.BarChart(
                    h=200,
                    dataKey="month",
                    data=data3,
                    type="percent",
                    series=[
                        {"name": "Smartphones", "color": "violet.6"},
                        {"name": "Laptops", "color": "blue.6"},
                        {"name": "Tablets", "color": "teal.6"}
                    ],
                    id="barchart_bar"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="barchart_card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.DonutChart(
                    data=data2,
                    withLabels=True,
                    withLabelsLine=True,
                    id="donut_chart"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="donut_card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.LineChart(
                    h=200,
                    dataKey="date",
                    data=data,
                    series=[
                        {"name": "Apples", "color": "indigo.6"},
                        {"name": "Oranges", "color": "blue.6"},
                        {"name": "Tomatoes", "color": "teal.6"}
                    ],
                    curveType="linear",
                    tickLine="xy",
                    withXAxis=False,
                    withDots=False,
                    id="line_chart"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="line_card",
            className="cardChart"
        ),
        dmc.Card(
            children=[
                dmc.PieChart(
                    data=data2,
                    withLabelsLine=True,
                    labelsPosition="inside",
                    labelsType="percent",
                    withLabels=True,
                    id="pie_chart"
                )
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"margin": "10px"},
            id="pie_card",
            className="cardChart"
        )
    ]
    return charts
