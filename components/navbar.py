from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
component = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("overview", href="/overview")),
            dbc.NavItem(dbc.NavLink("data", href="/data")),
            dbc.NavItem(dbc.NavLink("diagramm", href="/diagramm"))
        ],
        brand="Multipage Dash App",
        brand_href="/overview",
        color="primary",
        dark=True,
        fluid=True
    ),
])
