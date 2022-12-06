import dash
from dash import html,dcc
from matplotlib.colors import colorConverter
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pickle
from dash import Dash, dash_table
import pandas as pd


dash.register_page(__name__)


"""with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle) """

   

layout = html.Div(children=[
    html.H1(children='This is our Archive page'),
    html.Div(children='''
        This is our Archive page content.
    '''),

])