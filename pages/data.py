# Import necessary libraries 
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pickle
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle)

layout = dbc.Container(children=[dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "deletable": True} for i in testdatei.columns],
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
        
        data=testdatei.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_deletable=True,
        page_action="native",
        page_current= 0,
        style_table={'overflowY': 'auto'},
        page_size=20
    )])

