from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
component = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Overview", href="/Overview")),
            dbc.NavItem(dbc.NavLink("Data", href="/Data")),
            dbc.NavItem(dbc.NavLink("Plotting", href="/Plotting")),
            dbc.NavItem(dbc.NavLink("Project", href="/Project")),
        ],
        brand="10x Visualiser",
        brand_href="/Overview",
        color="primary",
        dark=True,
        fluid=True
    ),
])
