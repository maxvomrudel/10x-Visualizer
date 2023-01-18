import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table, dcc, html
import pandas as pd
from dash_bootstrap_templates import load_figure_template

load_figure_template("darkly")

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei = pickle.load(handle)

werte = testdatei.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)

fig1 = px.line(werte, x=werte.index, y="Estimated Number of Cells")
fig2 = px.line(werte, x=werte.index, y="Mean Reads per Cell")
fig3 = px.line(werte, x=werte.index, y="Median Genes per Cell")

werte2 = testdatei.groupby(["BfxProjekt"]).count()

fig4 = px.bar(werte2, x=werte2.index, y="Samplename")


def get_values(input):
    return sum(testdatei[input])


number_of_cells = get_values("Estimated Number of Cells")

table_content = [werte.shape[0], testdatei.shape[0], number_of_cells]
Index = [
    "1. Number of experiments", "2. Number of samples",
    "3. Total number of cells"
]

summary = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Overview", className="card-title"),
            html.P("Number of experiments: " + str(werte.shape[0])),
            html.P("Number of samples: " + str(testdatei.shape[0])),
            html.P("Total number of cells: " + str(number_of_cells))
        ]
        ),
    ],
    style={"width": "18rem"},
)

diagrams = html.Div(children=[
    html.Div(
        style={'textAlign': 'center'},
        children=[
            html.P("Estimated number of genes"),
            dcc.Graph(id="fig3", figure=fig3),
            html.H1("")
        ]),
    html.Div(
        style={"textAlign":"center"},
        children=[
            html.P("Number of samples"),
            dcc.Graph(id="fig4", figure=fig4),
            html.H1("")
        ]),
    html.Div(
        style={"textAlign":"center"},
        children=[
            html.P("Estimated number of cells"),
            dcc.Graph(id="fig1", figure=fig1),
            html.H1("")
        ]),
    html.Div(
        style={"textAlign":"center"},
        children=[
            html.P("Mean reads in cells"),
            dcc.Graph(id="fig2", figure=fig2),
            html.H1("")
        ]),
    html.Div("hello")
    ])

layout = dbc.Container([
    dbc.Row([
        dbc.Col(children=[summary], width=3),
        dbc.Col(children=[diagrams], width=9)
    ])
])


