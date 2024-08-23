from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify

def create_hover_card(icon, text1, text2, card_id):
    return dmc.HoverCard(
        children=[
            dmc.Card(
                children=[
                    dmc.Group(
                        children=[
                            html.Div(
                            DashIconify(icon=icon, width=10, className="cardIcon"),
                                className="cardIconContainer",

                            ),
                            dmc.Stack(
                                children=[
                                    dmc.Text(text1, size="xs", className="cardLabel"),
                                    dmc.Text(text2, size="lg", className="cardValue")
                                ],
                                gap="0px"

                            )
                        ],
                        align="center",

                    )
                ],
                shadow="sm",
                padding="md",
                radius="md",
                withBorder=True,
                style={"width": "200px"},
                className="statsCard",
                id=card_id,

            )
        ],
    )

hover_cards = html.Div(
    children=[
        create_hover_card("oi:people", "People impacted", "1,347", "hover-card-1"),
        create_hover_card("flowbite:dollar-outline", "Property value", "$120 M", "hover-card-2"),
        create_hover_card("fa-solid:road", "Road mileage", "85", "hover-card-3"),
        create_hover_card("clarity:building-solid", "Buildings", "835", "hover-card-4")
    ],
    style={"position": "absolute", "top": "10px", "left": "10px", "zIndex": 1000}
)

# Affix
stats_hover_card = dmc.Affix(
    children=hover_cards,
    position={"top": 0, "right": 250},
    zIndex=1000,
    id="stats-hover-card-affix"
)

