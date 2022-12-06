# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash import html,dcc
from matplotlib.colors import colorConverter
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pickle
from dash import Dash, dash_table
import pandas as pd


with open("metrics_summary(1).pickle", 'rb') as handle:
    testdatei= pickle.load(handle)
### Add the page components here 
table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
    
    ]
row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

page2_table = dbc.Table(table_header + table_body, bordered=True)

# Define the final page layout
layout = dbc.Container([
    dbc.Row([
        html.div(dash_table.DataTable(testdatei.to_dict('records'), [{"name": i, "id": i} for i in testdatei.columns])
        )
    ])
])