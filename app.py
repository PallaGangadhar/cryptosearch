import dash
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from graph import load_main_chart
from cat_page import cat_tabs


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dashboard - Cryptoresearch'
server = app.server
app.config.suppress_callback_exceptions = True
