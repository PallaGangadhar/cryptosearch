import dash
import flask

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


flask_server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server=flask_server)
app.title = 'Dashboard - Cryptoresearch'

server = app.server
app.config.suppress_callback_exceptions = True
