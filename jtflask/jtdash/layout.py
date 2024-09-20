from dash import html, dcc
import dash_mantine_components as dmc
from dash_extensions import DeferScript

from .sidebar import sidebar
from .statshovercards import stats_hover_card


layout = dmc.MantineProvider(
    html.Div(
        [
            DeferScript(src="../static/assets/js/main-defer.js"),
            html.Div(id="digital-twin-container"),
            dcc.Store(id="chart-data-store"),
            sidebar(),
            # stats_hover_card,
        ]
    )
)


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
                    {{%app_entry%}}
                    <footer>
                        {{%config%}}
                        {{%scripts%}}
                        {{%renderer%}}
                    </footer>
                </body>
            </html>
        """
