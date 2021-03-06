'''
This module handles routing of different pages in the dashboard and
is responsible for rendering correct modules as per user interaction
'''
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import graph
import graph_two
from cat_page import cat_tabs
from app import app


app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

# Callback for routing
@app.callback(Output('page-content', 'children'),
              [Input('url', component_property='pathname')])
def display_page(pathname):
    pathname = str(pathname)
    if pathname == '/':
        return cat_tabs
    elif pathname.startswith('/graph/storeofvalueindex'):
        chart_to_load = pathname.split('/')[-1]
        return graph.load_main_chart()
    elif pathname.startswith('/graph/gold_vs_sov'):
        chart_to_load = pathname.split('/')[-1]
        return graph_two.load_main_chart()


if __name__ == '__main__':
    app.run_server(debug=True)