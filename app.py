import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY],
                meta_tags=[{
                    "name": "viewport",
                    "content": "width=device-width"
                }],
                suppress_callback_exceptions=True)
