
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
import dash
import plotly.express as px
import pickle
from dash import Dash, dash_table, dcc, html
import pandas as pd
from dash import html
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container(
    [dbc.Row(
            [
                dbc.Col(html.Div(style= {"border":"double"}, children=[html.H1("overview")]), width=3),

                dbc.Col(html.Div(children=[
                    html.Div(style= {"border":"double"}, children=[
                         dbc.Row([
            
                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("Cells"),
                        ]),

                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("reads in cells")
                    ])

                    ])]),


                    html.Div(style= {"border":"double"}, children=[
                        dbc.Row([
            
                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("number of genes"),
                        ]),

                dbc.Col(style={"border":"double",'textAlign':'center'},children=[
                        html.P("number of samples")
                    ])

                    ])
                    ]),
                    html.Div("hello")
                ]), width=9),
            ]
        ),
    ]
)
app.run_server(debug=True)






content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Distribution of Categorical Variable'),
                        ]),
                dbc.Col(
                    [
                        html.P('Distribution of Continuous Variable')
                    ])
            ],
            style={"height": "50vh"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Correlation Matrix Heatmap')
                    ])
            ],
            style={"height": "50vh"}
            )
        ]
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ]
            ),
        ],
    fluid=True
    )


if __name__ == "__main__":
    app.run_server(debug=True, port=1234)