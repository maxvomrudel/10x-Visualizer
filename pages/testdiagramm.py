# Import necessary libraries
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
import pickle
from dash import dcc, html, callback
from dash.dependencies import Input, Output
import pandas as pd
from dash_bootstrap_templates import load_figure_template

load_figure_template("darkly")


dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei = pickle.load(handle)

werte = testdatei.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)
spalten = werte.select_dtypes(include="number").columns
arten= ["line","bar","scatter"]

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
    "margin-left": "20px",
    #"margin-right": "16px",
    #"padding": "2rem 1rem",
}

row = html.Div(
    dbc.Row([
        dbc.Col(style={'textAlign': 'center'},children = [
            dbc.DropdownMenu(
                    label = "Y Wert",
                    id="y-variable",
                    children=[
                        dbc.DropdownMenuItem(col) for col in spalten
                    ])],width = 4),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dbc.DropdownMenu(
                    label = "Type of diagram",
                    id="Diagrammart",
                    children=[
                        dbc.DropdownMenuItem(col) for col in spalten
                    ])],width = 4),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dbc.DropdownMenu(
                    label = "Value of the abscissa if scatter was choosen",
                    id= "x-scatter",
                    children=[
                        dbc.DropdownMenuItem(col) for col in spalten
                    ])],width = 4)
    ]))

@callback(
    Output("testdiagram", "figure"),
    [
        Input("y-variable", "value"),
        Input("Diagrammart", "value"),
        Input("x-scatter", "value")
    ],
)

def make_graph(y, Art,x):
    if Art=="line":
        print("Diagrammart: " + y)
        return px.line(werte, x=werte.index, y=y)
    elif Art=="scatter":
        print("Diagrammart: " + y)
        return px.scatter(werte, x=x, y=y, color=y)
    else:
        print("Diagrammart: " + y)
        return px.bar(werte, x=werte.index, y=y)

diagram = dcc.Graph(id="testdiagram", figure=fig, style={'height': "85vh", "width":"170vh",'textAlign': 'center' })


content = html.Div(html.Div(
    [diagram],
    style=CONTENT_STYLE))

layout = html.Div([
    html.H1(""),
    html.H1(""),
    row, 
    html.H1(""),
    html.H1(""),
    content
])