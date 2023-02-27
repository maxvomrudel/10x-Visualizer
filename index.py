from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
from pages import data, overview, testdiagramm, Projekt
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
    if path_name == '/overview':
        return overview.layout
    if path_name == '/data':
        return data.layout
    if path_name == '/Projekt':
        return Projekt.layout
    if path_name == '/testdiagramm':
        return testdiagramm.layout
    else:
        return (overview.layout)


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
