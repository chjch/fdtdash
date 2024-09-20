import dash_mantine_components as dmc
from dash import html
from .navbar import get_navbar
from .header import get_header

def appshell():
    header = get_header()
    navbar = get_navbar()

    return dmc.AppShell(
        [
            dmc.AppShellHeader(id="jaxtwin-header", children=[header]),
            dmc.AppShellNavbar(id="jaxtwin-navbar", children=[navbar]),
        ],
        zIndex=1400,
        padding="xl",
        header={
            "height": 70,
        },
        navbar={
            "width": 300,
            "breakpoint": "sm",
        },
        withBorder=False,
    )
