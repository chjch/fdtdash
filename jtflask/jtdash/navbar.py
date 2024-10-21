from dash import html, dcc
import dash_mantine_components as dmc
from .brand import get_brand
from .charts import get_charts
from .widgets import (
    get_arcgis_sketch_card,
    get_building_visualization_card,
    get_basemap_gallery,
)
from .utils import get_icon

NAVBAR_BUTTONS = {
    "charts": "charts-button",
    "hazard": "tools-button",
    "housing": "buildings-toggle-button",
    "health": "layers-toggle-button",
    "neighborhood": "clipboard-toggle-button",
    "legend": "legend-toggle-button",
    "basemap": "basemaps-gallery-button",
    "collapse": "collapse-button",
}

NAVBAR_PANELS = {
    "charts": get_charts(),
    "hazard": get_arcgis_sketch_card(),
    "housing": get_building_visualization_card(),
    "health": dmc.Card("Health", id="health-panel", className="hidden"),
    "neighborhood": dmc.Card("Neighborhood", id="neighborhood-panel", className="hidden"),
    "legend": dmc.Card("Legend", id="legend-panel", className="hidden"),
    "basemap": get_basemap_gallery(),
}


def get_navbar_buttons():
    return html.Div(
        id="navbar-buttons",
        children=[
            dmc.Button(
                id=NAVBAR_BUTTONS["charts"],
                children=get_icon(icon="carbon:chart-line-data"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["hazard"],
                children=get_icon("carbon:flood", "open-arcgis"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["housing"],
                children=get_icon("ph:buildings"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["health"],
                children=get_icon("fluent-mdl2:health"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["neighborhood"],
                children=get_icon("ph:park-light"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["legend"],
                children=html.Div(id="legend-svg"),
                className="navbar-button",
            ),
            dmc.Button(
                id=NAVBAR_BUTTONS["basemap"],
                children=html.Div(id="basemap-svg"),
                className="navbar-button",
            ),
        ],
    )


def get_navbar_collapse_button():
    return dmc.Button(
        id=NAVBAR_BUTTONS["collapse"],
        children=[
            get_icon(
                icon="heroicons:chevron-double-left-16-solid",
                icon_id="collapse-icon",
            )
        ],
        variant="default",
        fullWidth=False,
    )


def get_navbar_controls():  # Navbar Control: brand, buttons, collapse button
    navbar_brand = get_brand()
    navbar_icons = get_navbar_buttons()
    navbar_collapse = html.Div(
        id="collapse-button-container",
        children=get_navbar_collapse_button(),
    )
    return html.Div(
        id="navbar-control",
        children=[navbar_brand, navbar_icons, navbar_collapse],
    )


def get_navbar_panels():
    return html.Div(
        id="navbar-drawer",
        children=[*NAVBAR_PANELS.values()],
    )


# def get_navbar():
#     navbar_control = get_navbar_control()
#     navbar_drawer = get_navbar_content()
#
#     return html.Div(
#         id="navbar-container",
#         children=[
#             dcc.Store(
#                 id="drawer-content-store",
#                 data={"charts": "charts", "tools": "tools"},
#             ),
#             navbar_control,
#             navbar_drawer,
#         ],
#     )


def get_sidebar_left_column():
    sidebar_brand = html.Div(
        [
            get_icon(icon="solar:box-minimalistic-bold", icon_id="sidebar-brand-logo"),
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
                children=get_icon(icon="carbon:chart-line-data"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="arcgis-tools-toggle-button",
                children=get_icon("carbon:flood", "open-arcgis"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="buildings-toggle-button",
                children=get_icon("ph:buildings"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="layers-toggle-button",
                children=get_icon("fluent-mdl2:health"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="clipboard-toggle-button",
                children=get_icon("ph:park-light"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="legend-toggle-button",
                children=html.Div(id="legend-svg"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="basemap-gallery-toggle-button",
                children=html.Div(id="basemap-svg"),
                className="sidebar-icon",
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
    charts = get_charts()
    arcgis_building_stats_tool = get_building_visualization_card()
    basemap_gallery = get_basemap_gallery()

    scrollable_div_tools = html.Div(
        id="arcgistools_scrollable_div",
        className="mantine-Drawer-body-item hidden",
        children=[arcgis_sketch_tool_card],
    )
    scrollable_div_building_stats = html.Div(
        children=arcgis_building_stats_tool,
        id="scrollable_div_bulding_stats",
        className="mantine-Drawer-body-item hidden",
    )

    scrollable_div_drawer = dmc.Drawer(
        children=[
            charts,
            scrollable_div_tools,
            basemap_gallery,
            scrollable_div_building_stats,
        ],
        id="chart_scrollable_drawer",
        className="",
        padding="2",
        opened=True,
        keepMounted=True,
        closeOnClickOutside=False,
        closeOnEscape=False,
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
