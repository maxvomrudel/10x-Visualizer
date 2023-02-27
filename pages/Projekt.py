from dash import callback, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
import pickle
from dash_bootstrap_templates import load_figure_template

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle)

data = []
result = "bfx1966"
data = testdatei[testdatei["BfxProjekt"] == result]
    

dropdownValues = testdatei["BfxProjekt"].to_list()
projekts = []
for r in dropdownValues:
    if(projekts.count(r)<1):
        projekts.append(r)
    else:next


def get_values(data):
    return sum(data["Estimates Number of Cells"].tolist())


layout = html.Div(children = [
        dcc.Dropdown(
                    id="Projekt",
                    options=[
                        {"label": col, "value": col} for col in projekts
                    ],
                    value=projekts[0]
    ),
    html.Div(children=[
        dbc.Row([
            dbc.Col(chuildren=[
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Overview", className="card-title"),
                        html.P("Number of samples: " + str(len(data.index)) ),
                        html.P("Number of species: " + str(len(set(data["Species"].tolist())))),
                        html.P("Total number of cells: " + str(get_values(data)) )
            ])])])])])])

@callback(
    Output("r", "value0"),
    [
        Input("Projekt", "value")
    ],
)

def giveback(y):
    for r in projekts:
        if y == r:
            result = r
        else:
            next

    data = testdatei[testdatei["BfxProjekt"] == result]
    print(data)



@callback(
    Output("r", "value1"),
    [
        Input("Projekt", "value")
    ],
)

def giveback(y):
    for r in projekts:
        if y == r:
            result = r
        else:
            next

    data = testdatei[testdatei["BfxProjekt"] == result]
    print(data)







layout = dbc.Container([
    dbc.Row([
        
        dbc.Col(children=[dropdown])

    ])
])

"""dbc.Col(children=[summary]),"""


