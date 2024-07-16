import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import json

import os


def get_icon(icon, icon_id=None):
    if icon_id is None:
        return DashIconify(icon=icon)
    else:
        return DashIconify(icon=icon, id=icon_id)


# Function to read the SVG file content
def read_svg(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Read SVG file content
svg_path = "D:\\Projects\\jaxtwin\\jtflask\\static\\assets\\svg\\sidebar.svg"
svg_content = read_svg(svg_path)

# Load data from JSON file in assets folder
def load_data_from_assets(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Assuming the JSON file is in the `assets` folder
# data1path = dash.get_asset_url("data1.json")
# data = load_data_from_assets('assets/data/data.json')



sidebar_brand = html.Div(
    [
        DashIconify(icon="solar:box-minimalistic-bold", id="sidebar-brand-logo"),
        html.P(
            children=[
                html.Span('Jax', style={ "font-weight": "bolder"}),
                html.Span('Twin', style={"font-weight": "400"}),
            ],
            id="sidebar-brand-logo-text"
        )
    ],
    className="sidebar-brand sidebar-item",
    id="sidebar-brand"
)

sidebar_main = html.Div(
    [
        dmc.NavLink(
            id="sidebar-home",
            leftSection=get_icon(icon="fluent:data-pie-20-regular"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            leftSection=get_icon(icon="solar:routing-2-linear"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            leftSection=get_icon(icon="ph:buildings"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            leftSection=get_icon(icon="solar:clipboard-text-linear"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            leftSection=get_icon(icon="solar:layers-minimalistic-linear"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            leftSection=get_icon(icon="la:list-ul"),
                className="sidebar-icon",
            ),
        dmc.NavLink(
            leftSection=get_icon(icon="hugeicons:maps-square-01"),
            className="sidebar-icon",
        ),
    ],
    className="sidebar-main sidebar-item",
    id="sidebar-main",
)




collapse_button = dmc.Button(
    DashIconify(icon="heroicons:chevron-double-left-16-solid",
                id="collapse-icon"),
    id="collapse-button",
    variant="default",
    fullWidth=False,
)

collapse_button_container = html.Div(
    collapse_button,
    id="collapse-button-container",
    className="sidebar-item"
)

sidebar_main_container = html.Div(
    sidebar_main,
    id="sidebar-main-container"
)
data = [
  {"date": "Mar 22", "Apples": 2890, "Oranges": 2338, "Tomatoes": 2452},
  {"date": "Mar 23", "Apples": 2756, "Oranges": 2103, "Tomatoes": 2402},
  {"date": "Mar 24", "Apples": 3322, "Oranges": 986, "Tomatoes": 1821},
  {"date": "Mar 25", "Apples": 3470, "Oranges": 2108, "Tomatoes": 2809},
  {"date": "Mar 26", "Apples": 3129, "Oranges": 1726, "Tomatoes": 2290}
]

data2 = [
  { "name": "USA", "value": 400, "color": "indigo.6" },
  { "name": "India", "value": 300, "color": "yellow.6" },
  { "name": "Japan", "value": 100, "color": "teal.6" },
  { "name": "Other", "value": 200, "color": "gray.6" }
]

data3 = [
    {"month": "January", "Smartphones": 1200, "Laptops": 900, "Tablets": 200},
    {"month": "February", "Smartphones": 1900, "Laptops": 1200, "Tablets": 400},
    {"month": "March", "Smartphones": 400, "Laptops": 1000, "Tablets": 200},
    {"month": "April", "Smartphones": 1000, "Laptops": 200, "Tablets": 800},
    {"month": "May", "Smartphones": 800, "Laptops": 1400, "Tablets": 1200},
    {"month": "June", "Smartphones": 750, "Laptops": 600, "Tablets": 1000}
]

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
    ),

]

scrollable_div = html.Div(
    children=charts,
    id="chart_scrollable_div"
)


scrollable_div_drawer = dmc.Drawer(
    children=scrollable_div,
    id="chart_scrollable_drawer",
    padding="2",
    opened=True,
    keepMounted=True,
    closeOnClickOutside=False,
    withinPortal=False,
    withOverlay=False,
    withCloseButton=False,
    transitionProps={
        "transition": "slide-right",
        "duration": 500,
        "timingFunction": "ease",
    },
    zIndex=9999,
)

drawer_content = html.Div(
    [
        html.Div(
            [sidebar_brand, sidebar_main_container, collapse_button_container],
            id="sidebar-col1"
        ),
        scrollable_div_drawer

    ],
    id="drawer-body-grid",
)

def sidebar2():
    return dmc.Drawer(
        children=[drawer_content],
        id="drawer",
        padding=0,
        opened=True,
        withinPortal=False,
        position="left",
        closeOnClickOutside=False,  # Do not take focus or close on outside click
        withOverlay=False,  # Disable overlay to prevent taking focus
        withCloseButton=False,
        # transitionProps={
        #     "transition": "slide-left",
        #     "duration": 500,
        #     "timingFunction": "ease",
        # },
        zIndex=10000,
    )
