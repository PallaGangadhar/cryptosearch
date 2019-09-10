import dash
import flask

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]


flask_server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=flask_server)
app.title = 'Dashboard - Cryptoresearch'

server = app.server
app.config.suppress_callback_exceptions = True
