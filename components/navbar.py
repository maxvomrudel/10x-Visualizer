# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("overview", href="/overview")),
                dbc.NavItem(dbc.NavLink("data", href="/data")),
            ] ,
            brand="Multipage Dash App",
            brand_href="/overview",
            color="dark",
            dark=True,
        ), 
    ])

    return layout
