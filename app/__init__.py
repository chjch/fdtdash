from flask import Flask


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    return app
