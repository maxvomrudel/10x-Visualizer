# Import necessary libraries
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
import pickle
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei = pickle.load(handle)

werte = testdatei.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)
spalten = testdatei.columns

fig = px.line(werte, x=werte.index, y=spalten[0])


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "width": "25rem",
    "padding": "16px",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Settings", className="display-4"),
        html.Hr(),
        html.P(
            "select diagram parameters", className="lead"
        ),
        html.Div(
            [
                dbc.Label("Werte"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in spalten
                    ],
                    value=spalten[0],
                ),
            ]
        )
    ],
    style=SIDEBAR_STYLE,
)

diagram = dcc.Graph(id="diagram", figure=fig, style={})

content = html.Div(
    [diagram],
    style=CONTENT_STYLE)

layout = html.Div([
    sidebar, 
    content
])


@callback(
    Output("diagram", "figure"),
    [
        Input("y-variable", "value"),
    ],
)
def make_graph(y):
    print("Wert für Y: " + y)
    return px.line(werte, x=werte.index, y=y)
