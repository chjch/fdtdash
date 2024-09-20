from dash import html, dcc
import dash_mantine_components as dmc
from .basemap_gallery import get_basemap_gallery
from .charts import create_charts
from .widgets import get_arcgis_sketch_card
from .utils import get_icon


def get_sidebar_left_column():
    sidebar_brand = html.Div(
        [
            get_icon("solar:box-minimalistic-bold", "sidebar-brand-logo"),
            html.P(
                children=[
                    html.Span("Jax", style={"font-weight": "bolder"}),
                    html.Span("Twin", style={"font-weight": "400"}),
                ],
                id="sidebar-brand-logo-text",
            ),
        ],
        className="sidebar-brand sidebar-item",
        id="sidebar-brand",
    )

    sidebar_main = html.Div(
        className="sidebar-main sidebar-item",
        id="sidebar-main",
        style={"z": "20px"},
        children=[
            dmc.Button(
                id="charts-toggle-button",
                children=get_icon("fluent:data-pie-20-regular"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="arcgis-tools-toggle-button",
                children=get_icon("solar:routing-2-linear", "open-arcgis"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="buildings-toggle-button",
                children=get_icon("ph:buildings"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="clipboard-toggle-button",
                children=get_icon("solar:clipboard-text-linear"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="layers-toggle-button",
                children=get_icon("solar:layers-minimalistic-linear"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="legend-toggle-button",
                children=html.Div(id="legend-svg"),
                className="sidebar-icon"
            ),
            dmc.Button(
                id="basemap-gallery-toggle-button",
                children=html.Div(id="basemap-svg"),
                className="sidebar-icon"
            ),
        ],
    )

    collapse_button = dmc.Button(
        get_icon("heroicons:chevron-double-left-16-solid", "collapse-icon"),
        id="collapse-button",
        variant="default",
        fullWidth=False,
    )

    collapse_button_container = html.Div(
        collapse_button,
        id="collapse-button-container",
        className="sidebar-item",
    )

    return html.Div(
        [sidebar_brand, sidebar_main, collapse_button_container],
        id="sidebar-col1",
    )

def get_sidebar_drawer():

    arcgis_sketch_tool_card = get_arcgis_sketch_card()
    charts = create_charts()
    basemap_gallery = get_basemap_gallery()

    scrollable_div_tools = html.Div(
        id="arcgistools_scrollable_div",
        className="scrollable-div hidden",
        children=[arcgis_sketch_tool_card],
    )

    scrollable_div_drawer = dmc.Drawer(
        children=[
            charts,
            scrollable_div_tools,
            basemap_gallery,
        ],
        id="chart_scrollable_drawer",
        className="",
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
        zIndex=10000,
    )

    return scrollable_div_drawer

def sidebar():
    sidebar_left_column = get_sidebar_left_column()
    sidebar_drawer = get_sidebar_drawer()

    drawer_content = html.Div(
        [
            sidebar_left_column,
            sidebar_drawer,
            dcc.Store(
                id="drawer-content-store",
                data={"charts": "charts", "tools": "tools"},
            ),
        ],
        id="drawer-body-grid",
    )

    return html.Div(
        children=[drawer_content],
        id="drawer",
    )
