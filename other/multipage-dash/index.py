# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import Data, Overview

# Connect the navbar to the index
from components import navbar

# define the navbar
nav = navbar.navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content',style={"color":"pink","overflow":"scrol-x","background":"yellow"}, children=[]),
     
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/overview':
        return Overview.layout
    if pathname == '/data':
        return Data.layout
    else:
        return ("nü"
            "nü"
        "nü"
        "nü"
        "nü"
        "nü"
        "nü"
        "nü")
        

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True)
