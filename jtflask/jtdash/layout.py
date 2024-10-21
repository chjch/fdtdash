from dash import html, dcc
import dash_mantine_components as dmc
from dash_extensions import DeferScript

from .brand import get_brand
from .sidebar import get_navbar_controls, get_navbar_panels
# from .statshovercards import stats_hover_card

CHART_STORE_ID = "chart-data-store"
NAVBAR_STORE_ID = "drawer-content-store"


def jtdash_appshell():
    header = html.Div(id='header-container', children=[get_brand()])
    navbar = html.Div(
        id="navbar-container",
        children=[
            get_navbar_controls(),
            get_navbar_panels(),
            dcc.Store(
                id=NAVBAR_STORE_ID,
                data={"charts": "charts", "tools": "tools"},
            ),
        ],
    )
    return dmc.AppShell(
        [
            dmc.AppShellHeader(id="jaxtwin-header", children=[header]),
            dmc.AppShellNavbar(id="jaxtwin-navbar", children=[navbar]),
        ],
        zIndex=1400,
        padding="xl",
        header={
            "height": 50,
        },
        navbar={
            "width": 300,
            "breakpoint": "sm",
        },
        withBorder=False,
    )


layout = dmc.MantineProvider([
    jtdash_appshell(),
    DeferScript(src="../static/assets/js/main-defer.js"),
    # html.Div(id="digital-twin-container"),
    dcc.Store(id=CHART_STORE_ID),
    # sidebar(),
    # stats_hover_card,
])


def html_layout(with_splash=True):
    if with_splash:
        splash_html_string = """
        <div class='splash'>
            <div class='logo'>
                <div class="logo-text">
                    <h1 class='animate__animated animate__fadeIn animate__delay-1s'>Jax</h1>
                    <h1 class='animate__animated animate__fadeIn animate__delay-3s'>Twin.</h1>
                </div>
                <img class='logo-image' src='/jtdash/assets/images/splash-logo-image.png'/>
            </div>
        </div>
        """
    else:
        splash_html_string = ""

    return f"""
        <!DOCTYPE html>
            <html>
                <head>
                    {{%metas%}}
                    <title>{{%title%}}</title>
                    {{%favicon%}}
                    {{%css%}}
                    <link
                        rel="stylesheet"
                        href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
                    />
                </head>
                <style>
                    ._dash-loading {{
                        display: none; !important;
                    }}
                </style>
                <body>
                    {splash_html_string}
                    <div id='digital-twin-container'></div>
                    {{%app_entry%}}
                    <footer>
                        {{%config%}}
                        {{%scripts%}}
                        {{%renderer%}}
                    </footer>
                </body>
            </html>
        """
