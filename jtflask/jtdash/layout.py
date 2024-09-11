from dash import html, dcc
import dash_mantine_components as dmc
from dash_extensions import DeferScript, EventListener

from .sidebar import sidebar, get_sidebar_components
from .statshovercards import stats_hover_card

# Initialize sidebar components and store as globals
(
    global_sidebar_brand,
    global_sidebar_main_container,
    global_collapse_button_container,
    global_scrollable_div_charts,
    global_scrollable_div_tools,
    global_scrollable_div_basemapG,
    global_scrollable_div_building_stats,
) = get_sidebar_components()

layout = dmc.MantineProvider(
    html.Div(
        [
            DeferScript(src="../static/assets/js/main-defer.js"),
            html.Div(id="deckgl-container"),
            EventListener(
                id="arcgis-event-listener",
                events=[
                    {"event": "restore-sketch-tool"},
                    {"event": "hide-sketch-tool"},
                ],
            ),
            dcc.Store(id="arcgis-tool-state"),
            sidebar(
                global_sidebar_brand,
                global_sidebar_main_container,
                global_collapse_button_container,
                global_scrollable_div_charts,
                global_scrollable_div_tools,
                global_scrollable_div_basemapG,
                global_scrollable_div_building_stats,

            ),
            stats_hover_card,
        ]
    )
)

html_layout = '''
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
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
