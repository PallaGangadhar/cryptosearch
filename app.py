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

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

# Callback for routing
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return cat_tabs
    elif pathname == '/graph':
        return graph.load_main_chart()


if __name__ == '__main__':
    app.run_server(debug=True)