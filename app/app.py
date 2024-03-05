from dash import Dash, html
from dash_extensions import DeferScript


external_scripts = [
    {"src": "https://unpkg.com/deck.gl@latest/dist.min.js"},
    # {"src": "https://unpkg.com/@loaders.gl/i3s@3.3.1/dist/dist.min.js"},
    {"src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"},
    # {"src": "{{ url_for('static', filename='node_modules/@loaders.gl/i3s/dist/index.js') }}"}
]

external_stylesheets = [
    {
        "src": "https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css",
        "rel": "stylesheet",
    },
]

app = Dash(
    __name__,
    assets_folder="static/assets",
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    assets_ignore="script.js",
)

app.layout = html.Div([
    DeferScript(src="static/assets/js/script.js"),
    html.Div(id="deckgl-container"),
])

if __name__ == '__main__':
    app.run_server(debug=False)
