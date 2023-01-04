from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
from pages import data, overview, diagram
from components import navbar
import dash
import dash_bootstrap_components as dbc

# define the navbar
nav = navbar.navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav,
    html.Div(id='page-content', children=[]),
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(path_name):
    if path_name == '/overview':
        return overview.layout
    if path_name == '/data':
        return data.layout
    if path_name == '/diagramm':
        return diagram.layout
    else:
        return ()


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
