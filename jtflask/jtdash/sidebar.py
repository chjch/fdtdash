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
                html.Span('Twin', style={"font-family": "IBM Plex Sans Condensed", "font-weight": "500",}),
            ],
            style={"margin": "0 0 0.5rem"}
        )
    ],
    className="sidebar-brand"
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
)


def sidebar():
    return html.Div([sidebar_brand, sidebar_main], className="sidebar")
