
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table, dcc, html
import pandas as pd







with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle)


werte= testdatei.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)

fig1 = px.line(werte, x=werte.index , y = "Estimated Number of Cells")
fig2 = px.line(werte, x=werte.index , y = "Mean Reads per Cell")
fig3 = px.line(werte, x=werte.index , y = "Median Genes per Cell")
fig4 = px.line(werte, x=werte.index , y = "Median Genes per Cell")

def wertebekommen(input):
    #testdatei.groupby("samplename").apply(Summe += testdatei[input])
    Summe = sum(testdatei[input])
    return Summe




Numberofcells = wertebekommen("Estimated Number of Cells")


Tabelleninhalt =[werte.size, testdatei.size, Numberofcells]
Index = ["1. Number of experiments", "2. Number of samples", "3. Total number of cells"]


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [dbc.Row(
            [
                dbc.Col(html.Div(style= {"border":"double"}, children=[html.H1("overview"),
                
                
                
                
                
                #dash_table.DataTable(data={"name": Index, "id": Tabelleninhalt})
                ]), width=3),

                dbc.Col(html.Div(children=[
                    html.Div(style= {"border":"double"}, children=[
                         dbc.Row([
            
                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("Estimated number of cells"),
                        dcc.Graph(id="fig1",figure=fig1, style={})
                        ], width=6),

                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("Mean reads in cells"),
                        dcc.Graph(id="fig2",figure=fig2, style={})
                    ], width=6)

                    ])]),


                    html.Div(style= {"border":"double"}, children=[
                        dbc.Row([
            
                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("Estimated number of genes"),
                        dcc.Graph(id="fig3",figure=fig3, style={})
                        ], width=6),

                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("Number of samples"),
                        dcc.Graph(id="fig4",figure=fig4, style={})
                    ], width=6)

                    ])
                    ]),
                    html.Div("hello")
                ]), width=9),
            ]
        ),
    ]
)
app.run_server(debug=True)



if __name__ == "__main__":
    app.run_server(debug=True, port=1234)


