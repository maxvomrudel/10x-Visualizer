# Import necessary libraries
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei = pickle.load(handle)

werte = testdatei.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)

dia = px.line(werte, x=werte.index, y="Estimated Number of Cells")

settings = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Settings", className="card-title"),
            html.P(
                "hier kommen dann die einstellungen",
                className="card-text",
            ),
            dbc.Button("Apply", color="primary"),
        ]
        ),
    ],
    style={"width": "18rem"},
)

diagram = dcc.Graph(id="diagram", figure=dia, style={})

layout = dbc.Container([
    dbc.Row([
        dbc.Col(settings),
        dbc.Col(diagram)
    ])
])
