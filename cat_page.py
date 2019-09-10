'''
This module renders the category tabs on the index page of the dashboard
and handles loading of contents in each tabs
'''
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from app import app
from graph import thumbnail_chart


cat_tabs = html.Div(id='categoryMenu',
    children=[
        html.Div(
            html.H2(children='Crypto Dashboard'),
            className='dashboard-title'
        ),        
        dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='At A Glance', value='tab-1'),
                dcc.Tab(label='Series', value='tab-2'),
                dcc.Tab(label='Recent', value='tab-3'),
                dcc.Tab(label='All', value='tab-4'),
            ]
        ),
        html.Div(id='tabs-content')
    ], 
    className='category-tabs'
)

# Dashboard Index Page
new_tab_content = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Link('Different Crypto Currency Market Price VS BTC Closing Price',
                    href='/graph/DCCMPvBCP',
                    style={'text-decoration': 'none'}
                )
            ], className='item-title'),
            html.Div(children=[
                thumbnail_chart()
            ], className='item-thumbnail')
        ], className='item-wrapper')
    ], className='chart-list-item'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Link('Different Crypto Currency Market Price VS LTC Closing Price',
                    href='/graph/DCCMPvLCP',
                    style={'text-decoration': 'none'}
                )
            ], className='item-title'),
            html.Div(children=[
                thumbnail_chart()
            ], className='item-thumbnail')
        ], className='item-wrapper'),
    ], className='chart-list-item'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Link('Different Crypto Currency Market Price VS BTC-Cash Closing Price',
                    href='/graph/DCCMPvBCCP',
                    style={'text-decoration': 'none'}
                )
            ], className='item-title'),
            html.Div(children=[
                thumbnail_chart()
            ], className='item-thumbnail')
        ], className='item-wrapper'),
    ], className='chart-list-item'),

    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Link('Different Crypto Currency Market Price VS Gold Closing Price',
                    href='/graph',
                    style={'text-decoration': 'none'}
                )
            ], className='item-title'),
            html.Div(children=[
                thumbnail_chart()
            ], className='item-thumbnail')
        ], className='item-wrapper'),
    ], className='chart-list-item')    

], className='chart-list')


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return new_tab_content
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Coming Soon')
        ], style={'text-align': 'center', 'color': '#34e0af'})
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Coming Soon')
        ], style={'text-align': 'center', 'color': '#34e0af'})
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Coming Soon')
        ], style={'text-align': 'center', 'color': '#34e0af'})