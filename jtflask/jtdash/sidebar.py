from dash import html, dcc
import dash_mantine_components as dmc
from .basemap_gallery import get_basemap_gallery
from .charts import create_charts
from .widgets import (get_arcgis_sketch_card, get_arcgis_building_stats_card,
                      get_layer_texture_card, get_scene_layer_selection_card,
                      get_neighborhood_zoom_card)
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
                className="sidebar-icon",
            ),
            dmc.Button(
                id="arcgis-tools-toggle-button",
                children=get_icon("solar:routing-2-linear", "open-arcgis"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="buildings-toggle-button",
                children=get_icon("ph:buildings"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="clipboard-toggle-button",
                children=get_icon("solar:clipboard-text-linear"),
                className="sidebar-icon",
            ),
            dmc.Button(
                id="layers-toggle-button",
                children=get_icon("solar:layers-minimalistic-linear"),
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
        [
            html.Img(src="../static/assets/svg/navbarSVGmod.svg",
                     className="navbar-svg"),
            sidebar_brand,
            sidebar_main,
            collapse_button_container
        ],
        id="sidebar-col1",
    )


def get_sidebar_drawer():
    arcgis_sketch_tool_card = get_arcgis_sketch_card()
    charts = create_charts()
    arcgis_building_stats_tool = get_arcgis_building_stats_card()
    basemap_gallery = get_basemap_gallery()
    layer_texture_card = get_layer_texture_card()
    scene_layer_selection_card = get_scene_layer_selection_card()
    neighborhood_zoom_card = get_neighborhood_zoom_card()

    scrollable_div_tools = html.Div(
        id="arcgistools_scrollable_div",
        className="mantine-Drawer-body-item hidden",
        children=[arcgis_sketch_tool_card],
    )
    scrollable_div_building_stats = html.Div(
        children=arcgis_building_stats_tool,
        id="scrollable_div_building_stats",
        className="mantine-Drawer-body-item hidden",
    )
    srcollable_div_layer_tools = html.Div(
        children=[scene_layer_selection_card,
                  layer_texture_card,
                  neighborhood_zoom_card,
                  dcc.Store(id='map-action-store')
                  ],
        id="scrollable_div_layer_tools",
        className="mantine-Drawer-body-item hidden",
    )

    scrollable_div_drawer = dmc.Drawer(
        children=[
            charts,
            scrollable_div_tools,
            basemap_gallery,
            scrollable_div_building_stats,
            srcollable_div_layer_tools
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
