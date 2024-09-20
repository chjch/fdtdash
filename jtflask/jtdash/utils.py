from dash_iconify import DashIconify

def get_icon(icon, icon_id=None):
    return DashIconify(icon=icon, id=icon_id) if icon_id else DashIconify(icon=icon)