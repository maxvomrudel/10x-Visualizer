from dash import callback, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import plotly.graph_objects as go
import pickle
from dash_bootstrap_templates import load_figure_template


with open("data/metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle)

dropdownValues = testdatei["BfxProjekt"].to_list()
projekts = []
for r in dropdownValues:
    if(projekts.count(r)<1):
        projekts.append(r)
    else:next

y = "bfx1966"
result = 0
def giveback(y):
    for r in projekts:
        if y == r:
            result = r
        else:
            next
    return result
result = "bfx1966"
data = []
data = testdatei[testdatei["BfxProjekt"]== result]

print(data)
