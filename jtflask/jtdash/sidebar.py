
import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def get_icon(icon, icon_id=None):
    if icon_id is None:
        return DashIconify(icon=icon)
    else:
        return DashIconify(icon=icon, id=icon_id)

sidebar_brand = html.Div(
    [
        DashIconify(icon="fluent:city-16-filled", id="sidebar-brand-logo"),
        html.P(
            children=[
                html.Span('Jax', style={"font-family": "IBM Plex Sans Condensed", "font-style": "italic"}),
                html.Span('Twin', style={"font-family": "IBM Plex Sans Condensed", "font-weight": "500"}),
            ],
            style={"margin": "0 0 0.5rem"}
        )
    ],
    className="sidebar-brand",
    id="sidebar-brand"
)

sidebar_main = html.Div(
    [
        dmc.NavLink(
            id="sidebar-home",
            icon=get_icon(icon="fluent:data-pie-20-regular"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            icon=get_icon(icon="tabler:gauge"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            icon=get_icon(icon="solar:layers-minimalistic-linear"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            icon=get_icon(icon="f7:list-bullet"),
            className="sidebar-icon",
        ),
        dmc.NavLink(
            icon=get_icon(icon="mage:message-info-round"),
            className="sidebar-icon",
        ),
    ],
    className="sidebar-main",
    id="sidebar-main"
)

collapse_button = dmc.Button(
    DashIconify(icon="fluent:chevron-left-24-filled", id="collapse-icon", color="black"),
    id="collapse-button",
    variant="light",
    color="gray",
    compact=True,
    fullWidth=True,
    style={"margin": "auto", "display": "block"},

)

collapse_button_container = html.Div(
    collapse_button,
    id="collapse-button-container",
)

svgblur = html.Img(src=dash.get_asset_url('svg/sidebar.svg'),
                   id="svgblur")

drawer_content = dmc.SimpleGrid(
    cols=2,
    children=[
        html.Div(
            [sidebar_brand, sidebar_main
             ],
            style={"height": "100%"},
            id="sidebar-col1"
        ),
        collapse_button_container


    ],
    id="drawer-body",
    style={"height": "100%"}
)

def sidebar():
    return dmc.Drawer(
        children=[drawer_content],
        id="drawer",
        padding=0,
        opened=True,  # Start open
        size="80px",  # Initial size
        position="left",
        closeOnClickOutside=False,  # Do not take focus or close on outside click
        withOverlay=False,  # Disable overlay to prevent taking focus
        withCloseButton=False,
        transition="slide-left",
        transitionDuration=1000
    )
