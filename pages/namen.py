import dash
from dash import html,dcc
from matplotlib.colors import colorConverter
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pickle
from dash import Dash, dash_table
import pandas as pd

with open("metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle) 

   
dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Archive page'),

      dash_table.DataTable(testdatei.to_dict('records'), [{"name": i, "id": i} for i in testdatei.columns]),
    html.Div(children='''
        This is our Archive page content.
    '''),

])