import pickle
import statistics
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import callback, dash_table, dcc, html
from dash.dependencies import Input, Output
from dash_bootstrap_templates import load_figure_template

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    source= pickle.load(handle)

data = []
bfx = "bfx1966"
data = source[source["BfxProjekt"] == bfx]

fig1 = px.box(data, x="BfxProjekt", y="Estimated Number of Cells")
fig2 = px.box(data, x="BfxProjekt", y="Mean Reads per Cell")
fig3 = px.box(data, x="BfxProjekt", y="Median Genes per Cell")
fig4 = px.box(data, x="BfxProjekt", y="Valid Barcodes")

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

def get_values(data,value):
    return sum(data[value].tolist())

def getDate(data):
    dateset = list(set(data["SampleDate"].tolist()))
    for r in range(len(dateset)):
        dateset[r] = dateset[r].strftime("%Y-%m-%d")
    return dateset


dropdown = dcc.Dropdown(
                    id="Projekt", options=[{"label": col, "value": col} for col in projekts],
                    value=projekts[0])

card = dbc.Card(id="card",children=[
            dbc.CardBody([
                html.H4("Overview", className="capytrd-title"),
                html.P("Species: " + str(list(set(data["Species"].tolist()))[0]) ),
                html.P("Number of samples: " + str(len(data.index)) ),
                html.P("Total number of cells: " + str(get_values(data,"Estimated Number of Cells")) ),
                html.P("Prepdates: " + ", ".join(getDate(data)) ),
                html.P("Total number of reads: " + str(get_values(data,"Number of Reads")) ),
                html.P("Mean genes: " + str(statistics.mean(data["Median Genes per Cell"].tolist())) ),
            ])
        ])

table = dbc.Container(children=[
            html.H4("filtering help"),
            html.Div(html.Ul(children=[html.Li(l) for l in ["text columns: \"control\"",
                "numeric colums: \">4860\", \">=4860\",\"<4860\" ,\"=<4860\",\"=4860\"",
                "date colums: \"<2021-10-13\",..."]])),
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
                filter_action="native",
                page_current= 0,
                style_table={'overflowY': 'auto'},
                page_size=8
            )
        ])


diagram = dbc.Container(children = [
    	    dbc.Row(children = [
                dbc.Col(width = 4, children = [
                    html.Div(style={'textAlign': 'center'},children=[html.H5("Estimated Number of Cells")]),            
                    dcc.Graph(id="p_figure1", figure=fig1)
                ]),
                dbc.Col(width = 4, children = [
                    html.Div(style={'textAlign': 'center'},children=[html.H5("Mean Reads per Cell")]),
                    dcc.Graph(id="p_figure2", figure=fig2)
                ]),
                dbc.Col(width = 4, children = [
                    html.Div(style={'textAlign': 'center'},children=[html.H5("Median Genes per Cell")]),
                    dcc.Graph(id="p_figure3", figure=fig3)
                ]),
            ]),
            dbc.Row(children = [
                dbc.Col(width = 4, children = [
                    html.Div(style={'textAlign': 'center'},children=[html.H5("Valid Barcodes")]),
                    dcc.Graph(id="p_figure4", figure = fig4)
                    ]),
                dbc.Col(width = 4, children = [
    
                ]),
                dbc.Col(width = 4, children = [
    
                ]),
            ])
        ])



@callback(
    Output("card", "children"),
    Input("Projekt", "value"))

def updateCard(bfxProjekt):
    data = getData(bfxProjekt)
    card =dbc.CardBody([
                        html.H4("Overview", className="capytrd-title"),
                        html.P("Species: " + str(list(set(data["Species"].tolist()))[0]) ),
                        html.P("Number of samples: " + str(len(data.index)) ),
                        html.P("Total number of cells: " + str(get_values(data,"Estimated Number of Cells")) ),
                        html.P("Prepdates: " + ", ".join(getDate(data)) ),
                        html.P("Total number of reads: " + str(get_values(data,"Number of Reads")) ),
                        html.P("Mean genes: " + str(round(statistics.mean(data["Median Genes per Cell"].tolist()))) ),
                    ])
    return card

@callback(
    Output("table", "data"),
    [Input("Projekt", "value")]
)

def updateTable(bfxProjekt):
    data = getData(bfxProjekt)
    return data.to_dict("records")

@callback(
    Output("p_figure1", "figure"),
    Output("p_figure2","figure"),
    Output("p_figure3","figure"),
    Output("p_figure4", "figure"),
    Input("Projekt", "value")
)

def makePlots(bfxProjekt):
    data = getData(bfxProjekt)
    f1 = px.box(data, x="BfxProjekt", y="Estimated Number of Cells")
    f2 = px.box(data, x="BfxProjekt", y="Mean Reads per Cell")
    f3 = px.box(data, x="BfxProjekt", y="Median Genes per Cell")
    f4 = px.box(data, x="BfxProjekt", y="Valid Barcodes")
    return f1,f2,f3,f4



layout = dbc.Container(style={"border":"2px black solid"}, children = [
    dbc.Row(dropdown),
    dbc.Row(style={"border":"2px black solid"}, children = [
        dbc.Col(width = 3, children = [card]),
        dbc.Col(width = 9, children = [diagram])
    ]),
    dbc.Row(table)
])