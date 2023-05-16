from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
from pages import Data, Overview, Plotting, Project
from components import navbar
import dash
import dash_bootstrap_components as dbc

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar.component,
    html.Div(id='page-content', children=[]),
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(path_name):
    if path_name == '/Overview':
        return Overview.layout
    if path_name == '/Data':
        return Data.layout
    if path_name == '/Project':
        return Project.layout
    if path_name == '/Plotting':
        return Plotting.layout
    else:
        return (Overview.layout)


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
