from dash import html, dcc
import dash_mantine_components as dmc
from .basemap_gallery import get_basemap_gallery
from .charts import create_charts
from .tools import get_tools
from .utils import get_icon
from .brand import get_brand

def get_navbar_buttons():
    return html.Div(
        id="navbar-buttons",
        children=[
            dmc.Button(
                id="charts-button",
                leftSection=get_icon("fluent:data-pie-20-regular"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="tools-button",
                leftSection=get_icon("solar:routing-2-linear", "open-arcgis"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="buildings-button",
                leftSection=get_icon("ph:buildings"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="clipboard-button",
                leftSection=get_icon("solar:clipboard-text-linear"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="layers-button",
                leftSection=get_icon("solar:layers-minimalistic-linear"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="list-button",
                leftSection=get_icon("la:list-ul"),
                className="navbar-button",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="basemaps-gallery-button",
                className="navbar-button",
                **{"data-position": "center"},
                children=[html.Img(src="/jtdash/assets/svg/basemap_icon.svg")],
            ),
        ],
    )


def get_navbar_control():
    navbar_brand = get_brand()
    navbar_icons = get_navbar_buttons()

    collapse_button = dmc.Button(
        id="collapse-button",
        children=[
            get_icon(id="collapse-icon", icon="heroicons:chevron-double-left-16-solid")
        ],
        variant="default",
        fullWidth=False,
    )

    collapse_button_container = html.Div(
        id="collapse-button-container",
        children=[collapse_button],
    )

    return html.Div(
        id="navbar-control",
        children=[navbar_brand, navbar_icons, collapse_button_container],
    )


def get_navbar_drawer():
    charts = create_charts()
    basemap_gallery = get_basemap_gallery()
    tools = get_tools()

    return html.Div(
        children=[
            charts,
            tools,
            basemap_gallery,
        ],
        id="navbar-drawer",
    )


def get_navbar():
    navbar_control = get_navbar_control()
    navbar_drawer = get_navbar_drawer()

    return html.Div(
        id="navbar-container",
        children=[
            dcc.Store(
                id="drawer-content-store",
                data={"charts": "charts", "tools": "tools"},
            ),
            navbar_control,
            navbar_drawer,
        ],
    )
