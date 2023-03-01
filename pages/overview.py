import dash_bootstrap_components as dbc
from dash import html
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from datetime import date
from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output

load_figure_template("darkly")

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    source = pickle.load(handle)

#werte = source.groupby(["BfxProjekt"]).mean(numeric_only=True).apply(round)


numerischeSpalten = source.select_dtypes(include="number").columns
andereSpalten = source.select_dtypes(exclude="number").columns
werte = source.groupby("BfxProjekt").aggregate({s: 'mean' for s in numerischeSpalten} | {s: 'first' for s in andereSpalten})
werte=werte.sort_values("SampleDate")
fig1 = px.line(werte, x="SampleDate", y="Estimated Number of Cells")
fig2 = px.line(werte, x="SampleDate", y="Mean Reads per Cell")
fig3 = px.line(werte, x="SampleDate", y="Median Genes per Cell")
werte2 = source.groupby(["BfxProjekt"]).count()
werte2= werte2[["SampleDate"]]
werte2.rename(columns={"SampleDate":"Number of samples"}, inplace=True)
werte = pd.concat([werte, werte2], axis=1)
fig4 = px.line(werte, x="SampleDate", y="Number of samples")

def get_values(input):
    return sum(source[input])

number_of_cells = get_values("Estimated Number of Cells")

table_content = [werte.shape[0], source.shape[0], number_of_cells]
Index = [
    "1. Number of experiments", "2. Number of samples",
    "3. Total number of cells"
]

summary = dbc.Card(
    [
        dbc.CardBody([
            html.H4("Overview", className="card-title"),
            html.P("Number of experiments: " + str(werte.shape[0])),
            html.P("Number of samples: " + str(source.shape[0])),
            html.P("Total number of cells: " + str(number_of_cells))
        ]
        ),
    ],
    style={"width": "18rem"},
)

diagrams = html.Div(children=[
    html.Div([
        dcc.DatePickerRange(
            id='datePicker1',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2040, 9, 19),
            initial_visible_month=date(2021, 8, 5),
            end_date=date(2030, 1, 1)),
            html.Div(id='outputDatePicker1')
            ]),
  
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
            html.P("Number of Samples"),
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
@callback(
    Output('fig3', 'figure'),
    Input('datePicker1', 'start_date'),
    Input('datePicker1', 'end_date'))
def update_fig3(start_date, end_date):
    filteredValues= werte
    filteredValues['SampleDate'] = filteredValues['SampleDate'].astype('datetime64[ns]')
    if start_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]>=start_date]

    if end_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]<=end_date]
    
    fig3 = px.line(filteredValues, x="SampleDate", y="Median Genes per Cell")
    return fig3

@callback(
    Output('fig1', 'figure'),
    Input('datePicker1', 'start_date'),
    Input('datePicker1', 'end_date'))
def update_fig1(start_date, end_date):
    filteredValues= werte
    filteredValues['SampleDate'] = filteredValues['SampleDate'].astype('datetime64[ns]')
    if start_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]>=start_date]

    if end_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]<=end_date]
    
    fig1 = px.line(filteredValues, x="SampleDate", y="Estimated Number of Cells")
    return fig1

@callback(
    Output('fig2', 'figure'),
    Input('datePicker1', 'start_date'),
    Input('datePicker1', 'end_date'))
def update_fig2(start_date, end_date):
    filteredValues= werte
    filteredValues['SampleDate'] = filteredValues['SampleDate'].astype('datetime64[ns]')
    if start_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]>=start_date]

    if end_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]<=end_date]
    
    fig2 = px.line(filteredValues, x="SampleDate", y="Mean Reads per Cell")
    return fig2

@callback(
    Output('fig4', 'figure'),
    Input('datePicker1', 'start_date'),
    Input('datePicker1', 'end_date'))
def update_fig4(start_date, end_date):
    filteredValues= werte
    filteredValues['SampleDate'] = filteredValues['SampleDate'].astype('datetime64[ns]')
    if start_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]>=start_date]

    if end_date is not None:
        filteredValues=filteredValues[filteredValues["SampleDate"]<=end_date]
    
    fig4 = px.line(filteredValues, x="SampleDate", y="Number of samples")
    return fig4
