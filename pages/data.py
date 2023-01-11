# Import necessary libraries 
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from dash_bootstrap_templates import load_figure_template

load_figure_template("DARKLY")

dash.register_page(__name__)

with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle)

# Define the final page layout
layout =dbc.Container(
    #style={"overflow-x":"scroll"},
    children=[
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True} for i in testdatei.columns
        ],
        data=testdatei.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_deletable=True,
        page_action="native",
        page_current= 0,
    ),
    html.Div(id='datatable-interactivity-container')])