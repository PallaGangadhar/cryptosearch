import io
import base64
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from flask import request, send_file
from dash.dependencies import Input, Output
from datetime import date, timedelta, datetime

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
    title='Asset Allocation of Gold and Incrementum Store of Value Cryptocurrencies Portfolio',
    xaxis={'title': 'Time Period',
           'type': 'date',
           'rangeslider': {'visible': True},
           'gridcolor': 'rgb(98, 98, 98)'
           },
    yaxis={'title': 'Weighted Price in USD', 'gridcolor': 'rgb(98, 98, 98)'},
    showlegend=True,
    legend=go.layout.Legend(
        xanchor="auto",
        yanchor="auto",
        bgcolor='rgb(49, 48, 53)'
    ),
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
    href='https://twitter.com/intent/tweet?url=http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-facebook', n_clicks=0, className='fa fa-facebook fa-2x')],
    href='http://www.facebook.com/sharer.php?u=http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-reddit', n_clicks=0, className='fa fa-reddit fa-2x')],
    href='https://reddit.com/submit?url=http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-linkedin', n_clicks=0, className='fa fa-linkedin fa-2x fg-share-gtm')],
    href='https://www.linkedin.com/shareArticle?mini=true&url=http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov',
    target="_blank",
    style={'text-decoration': 'none', 'padding-left':'10px'}),

    html.A(title="",
    children=[html.I(id='share-email', n_clicks=0, className='fa fa-envelope fa-2x')],
    href='mailto:?Subject=Checkout%20this%20Awesome%20visualization%20from%20CryptoResearch&body=http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov',
    target="_top",
    style={'text-decoration': 'none', 'padding-left':'10px'}),
]

def load_main_chart():
    return html.Div(children=[
        html.Div(children=[
            html.H2('Incrementum Store of Value Crypto Index vs Bitcoin')
        ], className='main-title'),
        html.Div(children=[
            html.Details(id='export-data-three',
                children=[
                    html.Summary('Export Data'),
                    html.Ul(id='export-list-three', children=[])
                ], className='export-data-three-opts'
            ),

            html.Div(className='frequency-selector m-l-auto', children=[
                html.Label('Frequency:'),
                dcc.Dropdown(
                    id='freq-dropdown-three',
                    options=[
                        {'label': 'Daily', 'value': 'Daily'},
                        {'label': 'Weekly', 'value': 'Weekly'},
                        {'label': 'Monthly', 'value': 'Monthly'},
                        {'label': 'Quaterly', 'value': 'Quaterly'},
                    ],
                    value='Daily'
                ),
            ]),
            html.Div(className='quick-filters m-l-auto', children=[
                html.Button('YTD', id='button5',n_clicks_timestamp=0,style={'border':'none'}),
                html.Span('|'),
                html.Button('1Y', id='button3',n_clicks_timestamp=0,style={'border':'none'}),
                html.Span('|'),
                html.Button('5Y', id='button2',n_clicks_timestamp=0,style={'border':'none'}),
                html.Span('|'),
                html.Button('10Y', id='button4',n_clicks_timestamp=0,style={'border':'none'}),
                html.Span('|'),
                html.Button('MAX', id='button1',n_clicks_timestamp=0,style={'border':'none'}),
            ]),
            html.Div([
                dcc.DatePickerRange(
                    id='date-picker-range-three',
                    start_date=data.index.min(),
                    end_date=data.index.max(),
                    max_date_allowed=data.index.max(),
                    min_date_allowed=data.index.min(),
                    display_format='DD/MM/YYYY',
                ),
            ], className='m-l-auto'),
        ], className='date-and-export'),

        html.Div([
            dcc.Graph(
                id='gold-sov-asset-alloc',
                config={
                    'displaylogo': False,
                    'displayModeBar': True,
                    'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian'],
                },
                figure={
                    'data': [
                        go.Scatter(
                            x=data.index,
                            y=data['SOV_index'],
                            mode='lines'
                        ),
                        go.Scatter(
                            x=data.index,
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
            html.P('The volatility in the returns of a crypto strategy will change significantly \
                if gold is added to the investment strategy. Since gold is subject to significantly \
                lower price fluctuations, the overall volatility decreases as the share of gold \
                increases. In addition, the low correlation due to the well-known diversification \
                effect reduces fluctuations in portfolio return disproportionately.',
                className='source-description'),
            html.Span('Suggested Citation:', className='citation-title'),
            html.P('Incrementum AG, 30-Month Rolling Correlation Gold vs. Incrementum Store \
                of Value Crypto Index, retrieved from Crypto Research Report; \
                http://data.cryptoresearch.report/graph/asset_alloc_gold_vs_sov, September, 2019.', className='citation-info')
        ], className='graph-info'),

        html.Div(children=social_share_links, className='social-links'),
        
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
                        x=data.index,
                        y=data['SOV_index'],
                        mode='lines',
                        name='Weighted Price of all Crypto Currency',
                    ),
                    go.Scatter(
                        x=data.index,
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
    Output('gold-sov-asset-alloc', 'figure'),
    [
        Input('date-picker-range-three', 'start_date'),
        Input('date-picker-range-three', 'end_date'),
        Input('freq-dropdown-three', 'value')
    ])
def update_main_graph(start_date, end_date, data_freq):
    global data
    if data_freq == 'Monthly':
        temp_data = data.resample('M').mean()
        new_data = temp_data[(temp_data.index >= start_date) & (temp_data.index <= end_date)]
    elif data_freq == 'Quaterly':
        temp_data = data.resample('Q').mean()
        new_data = temp_data[(temp_data.index >= start_date) & (temp_data.index <= end_date)]
    elif data_freq == 'Weekly':
        temp_data = data.resample('W').mean()
        new_data = temp_data[(temp_data.index >= start_date) & (temp_data.index <= end_date)]
    else:
        new_data = data[(data.index >= start_date) & (data.index <= end_date)]

    return {
        'data': [
            go.Scatter(
                x=new_data.index,
                y=new_data['SOV_index'],
                mode='lines', 
                name='Incrementum Store of Value Crypto Index',
            ),
            go.Scatter(
                x=new_data.index,
                y=new_data['Btc_Close_Price'],
                mode='lines',
                name='Bitcoin Price'
            ),
        ], 'layout': main_graph_layout}


@app.callback(
    [
        Output('date-picker-range-three', 'start_date'), 
        Output('date-picker-range-three', 'end_date')
    ],
    [
        Input('button1', 'n_clicks_timestamp'),
        Input('button2', 'n_clicks_timestamp'),
        Input('button3', 'n_clicks_timestamp'),
        Input('button4', 'n_clicks_timestamp'),
        Input('button5', 'n_clicks_timestamp'),
        Input('freq-dropdown-three', 'value'),
    ])
def updatedate(btn1, btn2, btn3, btn4, btn5, data_freq):
    global data

    if data_freq == 'Monthly':
        new_data = data.resample('M').mean()
        max_date = new_data.index.max()
        min_date = new_data.index.min()

    if data_freq == 'Quaterly':
        new_data = data.resample('Q').mean()
        max_date = new_data.index.max()
        min_date = new_data.index.min()

    if data_freq == 'Weekly':
        new_data = data.resample('W').mean()
        max_date = new_data.index.max()
        min_date = new_data.index.min()

    else:
        max_date = data.index.max()
        min_date = data.index.min()


    if int(btn1) > int(btn2) and int(btn1) > int(btn3) and int(btn1) > int(btn4) and int(btn1) > int(btn5):
        # for max data
        return min_date,max_date
    elif int(btn2) > int(btn1) and int(btn2) > int(btn3) and int(btn2) > int(btn4) and int(btn2) > int(btn5):
        # for 5 year data
        return max_date-timedelta(days=5*365),max_date
    elif int(btn3) > int(btn1) and int(btn3) > int(btn2) and int(btn3) > int(btn4) and int(btn3) > int(btn5):
        # for 1 year data
        return max_date-timedelta(days=1*365),max_date
    elif int(btn4) > int(btn1) and int(btn4) > int(btn2) and int(btn4) > int(btn3) and int(btn4) > int(btn5):
        # for 10 year data
        return max_date-timedelta(days=10*365),max_date
    elif int(btn5) > int(btn1) and int(btn5) > int(btn2) and int(btn5) > int(btn3) and int(btn5) > int(btn4):
        # for YTD data
        return date(date.today().year, 1, 1),date.today()

    return data.index.min(),data.index.max()



@app.callback(
    Output('export-list-three', 'children'),
    [Input('export-data-three', 'n_clicks')])
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


