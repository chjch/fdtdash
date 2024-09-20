from dash import html
from .utils import get_icon

def get_brand():
    logo_icon = get_icon(icon="solar:box-minimalistic-bold")
    logo_text = html.P(
        className="sidebar-brand-logo-text",
        children=[
            html.Span("Jax", style={"font-weight": "bolder"}),
            html.Span("Twin", style={"font-weight": "400"}),
        ],
    )

    return html.Div(
        className="brand",
        children=[logo_icon, logo_text],
    )
