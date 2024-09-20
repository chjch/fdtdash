from dash_iconify import DashIconify

def get_icon(icon, id=None):
    return DashIconify(icon=icon, id=id) if id else DashIconify(icon=icon)