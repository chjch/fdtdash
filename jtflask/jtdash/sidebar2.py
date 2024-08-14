from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .charts import create_charts
from .arcgisJS_tools import get_arcgis_sketch_card

def get_icon(icon, icon_id=None):
    return DashIconify(icon=icon, id=icon_id) if icon_id else DashIconify(icon=icon)

def get_sidebar_components(app):
    charts = create_charts(app)
    arcgis_tools = get_arcgis_sketch_card()

    sidebar_brand = html.Div(
        [
            get_icon("solar:box-minimalistic-bold", "sidebar-brand-logo"),
            html.P(
                children=[
                    html.Span('Jax', style={"font-weight": "bolder"}),
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
                id="open-charts-drawer-link",
                leftSection=get_icon("fluent:data-pie-20-regular"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                id="open-arcgis-drawer-link",
                leftSection=get_icon("solar:routing-2-linear"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                leftSection=get_icon("ph:buildings"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                leftSection=get_icon("solar:clipboard-text-linear"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                leftSection=get_icon("solar:layers-minimalistic-linear"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                leftSection=get_icon("la:list-ul"),
                className="sidebar-icon",
            ),
            dmc.NavLink(
                leftSection=get_icon("hugeicons:maps-square-01"),
                className="sidebar-icon",
            ),
        ],
        className="sidebar-main sidebar-item",
        id="sidebar-main",
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
        className="sidebar-item"
    )

    sidebar_main_container = html.Div(
        sidebar_main,
        id="sidebar-main-container"
    )

    scrollable_div_charts = html.Div(
        children=charts,
        id="chart_scrollable_div"
    )

    scrollable_div_tools = html.Div(
        children=arcgis_tools,
        id="arcgistools_scrollable_div"
    )

    return sidebar_brand, sidebar_main_container, collapse_button_container, scrollable_div_charts, scrollable_div_tools

def sidebar2(app):
    sidebar_brand, sidebar_main_container, collapse_button_container, scrollable_div_charts, scrollable_div_tools = get_sidebar_components(app)

    scrollable_div_drawer = dmc.Drawer(
        children=scrollable_div_tools,
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
            scrollable_div_drawer,
            # dcc.Store(id='drawer-content-store', data='charts')
            dcc.Store(id='drawer-content-store', data={'charts': 'charts', 'tools': 'tools'})
        ],
        id="drawer-body-grid",
    )

    return dmc.Drawer(
        children=[drawer_content],
        id="drawer",
        padding=0,
        opened=True,
        withinPortal=False,
        position="left",
        closeOnClickOutside=False,
        withOverlay=False,
        withCloseButton=False,
        transitionProps={
            "transition": "slide-left",
            "duration": 500,
            "timingFunction": "ease",
        },
        zIndex=10000,
    )
