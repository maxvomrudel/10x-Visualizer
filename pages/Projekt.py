from dash import callback, dcc, html, dash_table
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
    source= pickle.load(handle)

data = []
bfx = "bfx1966"
data = source[source["BfxProjekt"] == bfx]
    

dropdownValues = source["BfxProjekt"].to_list()
projekts = []
for r in dropdownValues:
    if(projekts.count(r)<1):
        projekts.append(r)
    else:next

def getData(bfxProjekt):
    for r in projekts:
        if bfxProjekt == r:
            bfxProjekt = r
        else:
            next

    data = source[source["BfxProjekt"] == bfxProjekt]
    return data


def get_values(data):
    return sum(data["Estimated Number of Cells"].tolist())


layout = html.Div(children = [
        dcc.Dropdown(
                    id="Projekt",
                    options=[
                        {"label": col, "value": col} for col in projekts
                    ],
                    value=projekts[0]
    ),
    html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Card(id="card",children=[
                    dbc.CardBody([
                        html.H4("Overview", className="capytrd-title"),
                        html.P("Number of samples: " + str(len(data.index)) ),
                        html.P("Number of species: " + str(len(set(data["Species"].tolist()))) ),
                        html.P("Total number of cells: " + str(get_values(data)) ),
                        html.P("Date(s) of Execution: " + str(list(set(data["SampleDate"].tolist()))) ),
                        html.P("Type of Projekt: " + data["Type"].tolist()[0] ),
                    ])])],width=3),
            dbc.Col(children=[
                dbc.Container(children=[
                dash_table.DataTable(
                id= "table",
                columns=[{"name": i, "id": i} for i in data.columns],
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
        
                data=data.to_dict('records'),
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                page_action="native",
                page_current= 0,
                style_table={'overflowY': 'auto'},
                page_size=20
                )])],width=9

            )])])])

@callback(
    Output("card", "children"),
    [
        Input("Projekt", "value")
    ],
)

def updateCard(bfxProjekt):
    data = getData(bfxProjekt)
    card =dbc.CardBody([
                        html.H4("Overview", className="capytrd-title"),
                        html.P("Number of samples: " + str(len(data.index)) ),
                        html.P("Number of species: " + str(len(set(data["Species"].tolist())))),
                        html.P("Total number of cells: " + str(get_values(data)) ),
                        html.P("Date(s) of Execution: " + str(list(set(data["SampleDate"].tolist()))) ),
                        html.P("Type of Projekt: " + str(set(data["Type"].tolist())) ),
                    ])
    return card


@callback(
    Output("table", "data"),
    [Input("Projekt", "value")]
)

def updateTable(bfxProjekt):
    data = getData(bfxProjekt)
    return data.to_dict("records")
