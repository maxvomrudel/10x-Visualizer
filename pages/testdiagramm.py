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

load_figure_template("DARKLY")


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
    #"margin-left": "18rem",
   # "margin-right": "2rem",
    #"padding": "2rem 1rem",
}

"""sidebar = html.Div(
    [
        html.H2("Settings", className="display-4"),
        html.Hr(),
        html.P(
            "select diagram parameters", className="lead"
        ),
        html.Div(
            [
               
                      ]
        )
    ],
    style=SIDEBAR_STYLE,
)"""

row = html.Div(
        dbc.Row([dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in spalten
                    ],
                    
                    value=spalten[0],
            ),
        ],width = 4),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="Diagrammart",
                    options=[
                        {"label": col, "value": col} for col in arten
                    ],
                    value=arten[0],
                    
                ),
   ],width = 4),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="x-scatter", #für die x-Werte des Scattergraphen
                    options=[
                        {"label": col, "value": col} for col in spalten
                    ],
                    value=spalten[0]),

   ],width = 4)]))

diagram = dcc.Graph(id="testdiagram", figure=fig, style={'height': "85vh", "width":"180vh" })


content = html.Div(
    [diagram],
    style=CONTENT_STYLE)

layout = html.Div([
    row, 
    content
])


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

