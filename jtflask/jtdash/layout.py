from dash import html, dcc
import dash_mantine_components as dmc
from dash_extensions import DeferScript, EventListener

from .appshell import appshell


layout = dmc.MantineProvider(
    [
        appshell(),
        html.Div(
            [
                DeferScript(src="../static/assets/js/main-defer.js"),
                EventListener(
                    id="arcgis-event-listener",
                    events=[
                        {"event": "restore-sketch-tool"},
                        {"event": "hide-sketch-tool"},
                    ],
                ),
                dcc.Store(id="arcgis-tool-state"),
            ]
        ),
    ]
)

html_layout = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"
        />
    </head>
    <style>
        ._dash-loading {
            display: none; !important;
        }
    </style>
    <body>
        <div class='splash'>
            <div class='logo'>
                <div class="logo-text">
                    <h1 class='animate__animated animate__fadeIn animate__delay-1s'>Jax</h1>
                    <h1 class='animate__animated animate__fadeIn animate__delay-3s'>Twin.</h1>
                </div>
                <img class='logo-image' src='/jtdash/assets/images/splash-logo-image.png'/>
            </div>
        </div>
        <div id='digital-twin-container'></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
