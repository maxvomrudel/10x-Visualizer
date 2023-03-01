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
    source= pickle.load(handle)

layout = dbc.Container(fluid=True, children=[dash_table.DataTable(
        id='datatable-interactivity',
        columns=[{"name": i, "id": i, "type":"any"} for i in source.columns],
        style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': 'white'
    },
    style_data={
        'backgroundColor': 'rgb(50, 50, 50)',
        'color': 'white'
    },
        
        data=source.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        filter_action="native",
        page_action="native",
        page_current= 0,
        style_table={'overflowY': 'auto'},
        page_size=22
    )])

