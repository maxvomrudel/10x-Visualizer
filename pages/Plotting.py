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

# get all, numeric and non-numeric columns
every_column = source.columns
numeric_columns = source.select_dtypes(include="number").columns
not_numeric_columns = source.select_dtypes(exclude="number").columns.tolist()

# aggregate by BfxProjekt
def mean_and_round(x):
    return round(mean(x))

def first(x):
    return x[0]

agg_funkt = {}
for c in numeric_columns:
    agg_funkt[c] = 'mean'
for c in not_numeric_columns:
    agg_funkt[c] = 'first'
    
values = source.groupby(["BfxProjekt"], as_index=False).agg(agg_funkt)

# filter not_numeric_columns to what is allowed
not_numeric_columns.append("-")
not_numeric_columns.remove("SampleName")
not_numeric_columns.remove("Key")
not_numeric_columns.remove("Filename")

types = ["line","bar","scatter"]

fig = px.line(values, x=values.index, y=numeric_columns[0])

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
                        {"label": col, "value": col} for col in numeric_columns
                    ],
                value="Estimated Number of Cells"                        
                ),
        ]),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="Type of diagram",
                    options=[
                        {"label": col, "value": col} for col in types
                    ],
                    value=types[0],
                    
                )]),
   
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="x-scatter",
                    options=[
                        {"label": col, "value": col} for col in numeric_columns
                    ],
                    value=numeric_columns[0],
                    
                )]),

        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="color",
                    options=[
                        {"label": col, "value": col} for col in every_column
                    ],
                    value=every_column[0],
                    
                )]),
        dbc.Col(style={'textAlign': 'center'},children = [
            dcc.Dropdown(
                    id="facetting",
                    options=[
                        {"label": col, "value": col} for col in not_numeric_columns
                    ],
                    value="-",
                    
                )]),
    ])])


@callback(
    Output("output_diagram", "figure"),
    [
        Input("y-variable", "value"),
        Input("Type of diagram", "value"),
        Input("x-scatter", "value"),
        Input("color", "value"),
        Input("facetting", "value" )
    ],
)

def make_graph(y, type_of_diagram,x,z,f=None):
    if f == "-": f = None
    if type_of_diagram=="line":
        fig = px.line(values, x=values.index, y=y, facet_col=f, facet_col_wrap=2)
        fig.update_xaxes(matches=None)
        fig.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
        fig.update_yaxes(matches=None)
        fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
        return fig
    elif type_of_diagram=="scatter":
        fig = px.scatter(source, x=x, y=y, color=z, facet_col=f, facet_col_wrap=3)
        fig.update_xaxes(matches=None)
        fig.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
        fig.update_yaxes(matches=None)
        fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
        return fig
    else:
        fig = px.bar(values, x=values.index, y=y, facet_col=f, facet_col_wrap=2)
        fig.update_xaxes(matches=None)
        fig.for_each_xaxis(lambda xaxis: xaxis.update(showticklabels=True))
        fig.update_yaxes(matches=None)
        fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True))
        return fig
    
diagram = dcc.Graph(id="output_diagram", figure=fig, style={'height': "85vh", "width":"170vh",'textAlign': 'center' })

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