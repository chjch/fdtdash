import dash_mantine_components as dmc
from dash import html
from .brand import get_brand


def get_header():
    brand = get_brand()

    return html.Div(id='header-container', children=[brand])
