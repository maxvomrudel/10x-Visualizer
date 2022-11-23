
import dash
from dash import html,dcc
from matplotlib.colors import colorConverter
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pickle
from dash import Dash, dash_table
import pandas as pd

#setup
with open("metrics_summary.pickle", 'rb') as handle:
    testdatei= pickle.load(handle) 


grouplist = ["Estimated Number of Cells","Mean Reads per Cell","Median Genes per Cell","Number of Reads","Valid Barcodes","Sequencing Saturation","Q30 Bases in Barcode","Q30 Bases in RNA Read","Q30 Bases in UMI","Reads Mapped to Genome","Reads Mapped Confidently to Genome","Reads Mapped Confidently to Intergenic Regions","Reads Mapped Confidently to Intronic Regions","Reads Mapped Confidently to Exonic Regions","Reads Mapped Confidently to Transcriptome","Reads Mapped Antisense to Gene","Fraction Reads in Cells","Total Genes Detected","Median UMI Counts per Cell","Filename","BfxProjekt","Samplename","Type"]
colorlist = ["Estimated Number of Cells","Mean Reads per Cell","Median Genes per Cell","Number of Reads","Valid Barcodes","Sequencing Saturation","Q30 Bases in Barcode","Q30 Bases in RNA Read","Q30 Bases in UMI","Reads Mapped to Genome","Reads Mapped Confidently to Genome","Reads Mapped Confidently to Intergenic Regions","Reads Mapped Confidently to Intronic Regions","Reads Mapped Confidently to Exonic Regions","Reads Mapped Confidently to Transcriptome","Reads Mapped Antisense to Gene","Fraction Reads in Cells","Total Genes Detected","Median UMI Counts per Cell","Filename","BfxProjekt","Samplename","Type"]
#colorlist = ["Estimated Number of Cells"]
fig1 = px.line(testdatei, x="Samplename", y = "Estimated Number of Cells")
fig2 = px.line(testdatei, x="Samplename", y = "Fraction Reads in Cells")
fig3 = px.line(testdatei, x="Samplename", y = "Median Genes per Cell")
labels = ["a","b"]
labels2 = ["c","d"]

#layout
app = dash.Dash()
app.layout = html.Div(className='row', children=
    [html.Div('hallo'),
                       html.H1('Test'),
                       html.Div(dcc.Dropdown(id='dropdown', options = labels)),
                       html.Div(id="content")])



"""
                       #html.Div(dcc.Dropdown(id='dropdown', options = labels)),
                       #html.Div(dcc.Dropdown(id='dropdown2', options = labels2)),
                       #dcc.Graph(id='fig1', figure=fig1),
                       #dcc.Graph(id='fig2', figure=fig2),
                       dcc.Graph(id='fig3', figure=fig3),
                       
                       html.Div(children=[
        dcc.Graph(id="fig2",figure=fig2, style={'display': 'inline-block'}),
        dcc.Graph(id="fig1",figure=fig1, style={'display': 'inline-block'})]),
       dash_table.DataTable(testdatei.to_dict('records'), [{"name": i, "id": i} for i in testdatei.columns])                
                       
                       
                       
                       
                       ])"""
                       
                    




#def update_graph(collum_name):
#    fig = px.line(testdatei, x="Samplename", y = "Estimated Number of Cells",  color = collum_name)
#    return fig
   

@app.callback(Output('fig2', 'figure'), Input('dropdown2', 'value'))
def update_graph(collum_name):
    return collum_name
"""
@app.callback(Output('fig3', 'figure'), Input('dropdown2', 'value'))
def update_graph(collum_name):
    fig = px.line(testdatei, x="Samplename", y = "Median Genes per Cell", color=collum_name)
    return fig
"""
app.run_server(debug=True)

