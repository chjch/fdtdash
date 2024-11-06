from dash_iconify import DashIconify


def get_icon(icon, icon_id=None, height_val=16, width_val=16):
    return (
        DashIconify(icon=icon, id=icon_id, height=height_val, width=width_val)
        if icon_id
        else DashIconify(icon=icon, height=height_val, width=width_val)
    )
