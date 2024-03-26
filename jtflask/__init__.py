from flask import Flask
from flask_cors import CORS


def init_app():  # init a flask app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    CORS(app)

    with app.app_context():
        from . import routes

        # init a dash app inside the flask app
        from .jtdash import init_dashboard
        app = init_dashboard(app)

        return app
