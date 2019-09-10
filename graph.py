import io
import base64
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from flask import request, send_file
from dash.dependencies import Input, Output

from data_store import process_and_get_crypto_data
from app import app


##########################################
########    Data Initialization    #######
##########################################
data = process_and_get_crypto_data()


##########################################
####  Define all layouts from below  #####
##########################################

main_graph_layout = go.Layout(
    title='Incrementum Store of Value Crypto Index',
    xaxis={'title': 'Time Period',
           'type': 'date',
           'rangeslider': {'visible': True},
           'rangeselector': {'visible': True,
                             'bgcolor': 'rgb(49, 48, 53)',
                             'bordercolor': 'rgb(51, 224, 167)',
                             'buttons':
                             [
                                 {'count': 1, 'step': 'year', 'label': '1Y'},
                                 {'count': 5, 'step': 'year', 'label': '5Y'},
                                 {'count': 10, 'step': 'year', 'label': '10Y'},
                                 {'step': 'all', 'label': 'Max'}
                             ]
                             },
           'gridcolor': 'rgb(98, 98, 98)'
           },
    yaxis={'title': 'Weighted Price in USD', 'gridcolor': 'rgb(98, 98, 98)'},
    showlegend=True,
    legend=go.layout.Legend(
        # x=2,
        # y=1.3,
        xanchor="auto",
        yanchor="auto",
        bgcolor='rgb(49, 48, 53)'
    ),
    # plot_bgcolor = 'rgb(229, 236, 246)',
    paper_bgcolor='rgb(49, 49, 53)',
    plot_bgcolor='rgb(49, 49, 53)',
    font={
        'color': 'rgb(52,224,175)',
        'size': 12
    },
    margin=go.layout.Margin(l=40, r=0, t=100, b=40)
)

social_share_links = [
    html.A(title="",
    children=[html.I(id='share-twitter', n_clicks=0, className='fa fa-twitter fa-2x')],
    href='https://twitter.com/intent/tweet?url=http://data.cryptoresearch.report/graph/DCCMPvBCP',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-facebook', n_clicks=0, className='fa fa-facebook fa-2x')],
    href='http://www.facebook.com/sharer.php?u=http://data.cryptoresearch.report/graph/DCCMPvBCP',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-reddit', n_clicks=0, className='fa fa-reddit fa-2x')],
    href='https://reddit.com/submit?url=http://data.cryptoresearch.report/graph/DCCMPvBCP',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-linkedin', n_clicks=0, className='fa fa-linkedin fa-2x fg-share-gtm')],
    href='https://www.linkedin.com/shareArticle?mini=true&url=http://data.cryptoresearch.report/graph/DCCMPvBCP',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-email', n_clicks=0, className='fa fa-envelope fa-2x')],
    href='mailto:?Subject=Checkout%20this%20Awesome%20visualization%20from%20CryptoResearch&body=http://data.cryptoresearch.report/graph/DCCMPvBCP',
    target="_top",
    style={'text-decoration': 'none', 'padding-left':'10px'}),
]

def load_main_chart():
    return html.Div(children=[
        html.Div(children=[
            html.H2('Different Crypto Currency Market Price VS BTC Closing Price')
        ], className='main-title'),
        html.Div(children=[
            html.Div(children=social_share_links, className='social-links'),

            html.Details(id='export-data',
                children=[
                    html.Summary('Export Data'),
                    html.Ul(id='export-list', children=[])
                ], className='export-data-opts'
            ),

            html.Div([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    start_date=data['Date'].min(),
                    end_date=data['Date'].max(),
                    max_date_allowed=data['Date'].max(),
                    min_date_allowed=data['Date'].min(),
                    display_format='DD/MM/YYYY',
                ),
            ], className='m-l-auto'),
        ], className='date-and-export'),

        html.Div([
            dcc.Graph(
                id='example-graph',
                config={
                    'displaylogo': False,
                    'displayModeBar': True,
                    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian'],
                },
                figure={
                    'data': [
                        go.Scatter(
                            x=data['Date'],
                            y=data['Weighted_Price'],
                            mode='lines'
                        ),
                        go.Scatter(
                            x=data['Date'],
                            y=data['Btc_Close_Price'],
                            mode='lines',
                            fillcolor='rgb(24, 128, 56)'
                        ),
                    ],
                    'layout': main_graph_layout
                },
            )], 
            style={'margin': 0}
        ),

        html.Div(id='graph-info', children=[
            html.Span('Source:', className='source-title'),
            html.Span('Coinmarketcap.com, Incrementum AG', className='sources'),
            html.P('The Incrementum Store of Value Index is a market capitalization \
                weighted index comprising of all non-Turing complete cryptocurrencies \
                with at least two out of three criteria met including market capitalization \
                of $500,000 or higher, market trading for 365 days or greater, and market \
                trading on two exchanges or more. Privacy coins are excluded. \
                The three coins in the index are Bitcoin, Bitcoin Cash, and Litecoin.',
                className='source-description'),
            html.Span('Suggested Citation:', className='citation-title'),
            html.P('Incrementum AG, Incrementum Store of Value Crypto Index, retrieved \
                from Crypto Research Report; http://data.cryptoresearch.report/graph/DCCMPvBCP, \
                September, 2019.', className='citation-info')
        ], className='graph-info')
    ], className='detailed-graph')

def thumbnail_chart():
    g = html.Div(
        children=[dcc.Graph(
            config={
                'displayModeBar': False
            },
            figure={
                'data': [
                    go.Scatter(
                        x=data['Date'],
                        y=data['Weighted_Price'],
                        mode='lines',
                        name='Weighted Price of all Crypto Currency',
                    ),
                    go.Scatter(
                        x=data['Date'],
                        y=data['Btc_Close_Price'],
                        mode='lines',
                        name='Bitcoin Price'
                    ),
                ],
                'layout': go.Layout(
                    xaxis={'showticklabels': False},
                    yaxis={'showticklabels': False},
                    showlegend=False,
                    height=90,
                    width=120,
                    margin=go.layout.Margin(l=0, r=10, t=0, b=30),
                    paper_bgcolor='rgb(49, 49, 53)',
                    plot_bgcolor='rgb(229, 236, 246)',
                )
            }
        )
        ], className='charts-thumbnail')
    return g


##########################################
#####  Define all callbacks below   ######
##########################################

# Callback for main Graph
@app.callback(
    Output('example-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    global data
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return {
        'data': [
            go.Scatter(
                x=data['Date'],
                y=data['Weighted_Price'],
                mode='lines', 
                name='Incrementum Store of Value Crypto Index',
            ),
            go.Scatter(
                x=data['Date'],
                y=data['Btc_Close_Price'],
                mode='lines',
                name='Closing Price of Bitcoin'
            ),
        ], 'layout': main_graph_layout}


@app.callback(
    Output('export-list', 'children'),
    [Input('export-data', 'n_clicks')])
def update_download_data(value):
    global data
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    csv_filename = 'data.csv'
    excel_filename = 'data.xls'
    path_to_file = 'data:text/csv;base64,' + payload

    return [
        html.Li([
            html.A('CSV',
                href=path_to_file, download=csv_filename)], className='download-link'),
        html.Li([
            html.A('Excel',
                href=path_to_file, download=excel_filename)], className='download-link'),
    ]                

