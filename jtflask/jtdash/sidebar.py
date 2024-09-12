from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .charts import create_charts
from .widgets import get_arcgis_sketch_card


def get_icon(icon, icon_id=None):
    return (
        DashIconify(icon=icon, id=icon_id)
        if icon_id
        else DashIconify(icon=icon)
    )


def get_sidebar_components():
    charts = create_charts()
    arcgis_tools = get_arcgis_sketch_card()

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
        [
            dmc.Button(
                id="charts-toggle-button",
                leftSection=DashIconify(
                    icon="fluent:data-pie-20-regular", width="24px"
                ),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="arcgis-tools-toggle-button",
                leftSection=get_icon("solar:routing-2-linear", "open-arcgis"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="buildings-toggle-button",
                leftSection=get_icon("ph:buildings"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="clipboard-toggle-button",
                leftSection=get_icon("solar:clipboard-text-linear"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="layers-toggle-button",
                leftSection=get_icon("solar:layers-minimalistic-linear"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="list-toggle-button",
                leftSection=get_icon("la:list-ul"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
            dmc.Button(
                id="maps-toggle-button",
                leftSection=get_icon("hugeicons:maps-square-01"),
                className="sidebar-icon",
                **{"data-position": "center"},
            ),
        ],
        className="sidebar-main sidebar-item",
        id="sidebar-main",
        style={"z": "20px"},
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

    scrollable_div_hidden = html.Div(
        id="scrollable-div-hidden", className="scrollable-div"
    )

    scrollable_div_charts = html.Div(
        children=charts, id="chart_scrollable_div", className="scrollable-div"
    )

    scrollable_div_tools = html.Div(
        children=arcgis_tools,
        id="arcgistools_scrollable_div",
        className="scrollable-div hidden",
    )
    
    # Container to hold basemap gallery
    basemap_gallery_container =  html.Div(
        id="basemap-gallery-container",
        className="scrollable-div hidden",
    )

    return (
        sidebar_brand,
        sidebar_main,
        collapse_button_container,
        scrollable_div_charts,
        scrollable_div_tools,
        basemap_gallery_container
    )


def sidebar(
    sidebar_brand,
    sidebar_main,
    collapse_button_container,
    scrollable_div_charts,
    scrollable_div_tools,
    basemap_gallery_container
):
    scrollable_div_drawer = dmc.Drawer(
        children=[
            scrollable_div_charts,
            scrollable_div_tools,
            basemap_gallery_container
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

    drawer_content = html.Div(
        [
            html.Div(
                [sidebar_brand, sidebar_main, collapse_button_container],
                id="sidebar-col1",
            ),
            scrollable_div_drawer,
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
