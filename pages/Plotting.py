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
    source = pickle.load(handle)

werte = source.groupby(["BfxProjekt"]).mean().apply(round)
numerischeSpalten = werte.select_dtypes(include="number").columns
arten= ["line","bar","scatter"]
alleSpalten = source.columns
nichtnumerischeSpalten = source.select_dtypes(exclude="number").columns.tolist()
nichtnumerischeSpalten.append("-")


fig = px.line(werte, x=werte.index, y=numerischeSpalten[0])

SIDEBAR_STYLE = {
    "width": "25rem",
    "padding": "16px"
}
CONTENT_STYLE = {
    #"margin-left": "20px"
}

row = html.Div(children=[
    dbc.Row([
        dbc.Col(style={'textAlign': 'center'},children=[
            html.H6("Y")
        ]),
            
        dbc.Col(style={'textAlign': 'center'},children=[
            html.H6("Type of diagram")
        ]),
   
        dbc.Col(style={'textAlign': 'center'},children=[
            html.H6("X (only in scatter)")
        ]),

        dbc.Col(style={'textAlign': 'center'},children=[
            html.H6("color (only in scatter)")
        ]),
        dbc.Col(style={'textAlign': 'center'},children=[
            html.H6("facetting (only in scatter)")
        ])
    ]),
    dbc.Row([
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in numerischeSpalten
                    ],
                value="Estimated Number of Cells"                        
                ),
        ]),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="Type of diagram",
                    options=[
                        {"label": col, "value": col} for col in arten
                    ],
                    value=arten[0],
                    
                )]),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="x-scatter",
                    options=[
                        {"label": col, "value": col} for col in numerischeSpalten
                    ],
                    value=numerischeSpalten[0],
                    
                )]),

        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="color",
                    options=[
                        {"label": col, "value": col} for col in alleSpalten
                    ],
                    value=alleSpalten[0],
                    
                )]),
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="facetting",
                    options=[
                        {"label": col, "value": col} for col in nichtnumerischeSpalten
                    ],
                    value="-",
                    
                )]),
    ])])


@callback(
    Output("testdiagram", "figure"),
    [
        Input("y-variable", "value"),
        Input("Type of diagram", "value"),
        Input("x-scatter", "value"),
        Input("color", "value"),
        Input("facetting", "value" )
    ],
)

def make_graph(y, Art,x,z,f):
    if Art=="line":
        return px.line(werte, x=werte.index, y=y)
    elif Art=="scatter":
        if f != "-":
            return px.scatter(source, x=x, y=y, color=z, facet_col=f)
        else:
            return px.scatter(source, x=x, y=y, color=z)
    else:
        return px.bar(werte, x=werte.index, y=y)

diagram = dcc.Graph(id="testdiagram", figure=fig, style={'height': "85vh", "width":"170vh",'textAlign': 'center' })

content = dbc.Container(
    [diagram],
    style=CONTENT_STYLE,
    fluid = True)

layout = html.Div([
    html.H1(""),
    html.H1(""),
    row, 
    html.H1(""),
    html.H1(""),
    content
])