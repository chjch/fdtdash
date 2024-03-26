from os import path

BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))


class Config:

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"


