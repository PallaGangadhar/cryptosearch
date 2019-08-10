import base64  
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from data_store import process_and_get_crypto_data
from app import app


data = process_and_get_crypto_data()

options = {
	'scrollZoom': True, # lets us scroll to zoom in and out - works
	'showLink': False, # removes the link to edit on plotly - works
	'modeBarButtonsToRemove': ['zoom2d', 'pan', 'pan2d', 'autoScale2d'],
	# //'modeBarButtonsToAdd': ['lasso2d'],
	'displayLogo': False, # this one also seems to not work
	'displayModeBar': True, # this one does work
}

def test_func():
    return 'function(){window.alert();}'

def load_main_chart():
    return html.Div(children=[
        html.Div(children=[
            html.H2('Different Crypto Currency Market Price VS BTC Closing Price')
        ], className='main-title'),
        html.Div(children=[
            html.Div([
                dcc.Dropdown(
                    id='export-dropdown',
                    options=[
                        {'label': 'Export as CSV', 'value': 'csv'},
                        {'label': 'Export as Excel', 'value': 'xlsx'},
                        {'label': 'Export as JSON', 'value': 'json'}
                    ],
                    value='',
                    style={ 'width': 200 }
                ),
                html.Div(id='download-button-container'),
            ], className='for-download',),
            html.Div([
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    start_date=data['Date'].min(),
                    end_date=data['Date'].max(),
                    max_date_allowed=data['Date'].max(),
                    min_date_allowed=data['Date'].min(),
                    display_format='DD/MM/YYYY',
                ),
            ],className='m-l-auto'),    
        ], className='date-and-export'),

        html.Div([
            dcc.Graph(
            id='example-graph',
            config={
                'displaylogo': False,
                'displayModeBar': True,
                'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian'],
            },
            figure= {
                'data' : [
                        go.Scatter(
                            x = data['Date'],
                            y = data['Weighted_Price'],
                            mode = 'lines'
                        ),
                        go.Scatter(
                            x = data['Date'],
                            y = data['Btc_Close_Price'],
                            mode = 'lines',
                            fillcolor = 'rgb(24, 128, 56)'
                        ),
                    ],
                'layout' : go.Layout(
                    title='Different Crypto Currency Market Price VS BTC Closing Price',
                    xaxis={'title': 'Time Period',
                            'type' : 'date',
                            'rangeslider': {'visible':True},
                            'rangeselector': {'visible':True, 
                                'buttons':
                                    [
                                        {'count':1,'step':'year','label':'1Y'},
                                        {'count':5,'step':'year','label':'5Y'},
                                        {'count':10,'step':'year','label':'10Y'},
                                        {'step':'all','label':'Max'}
                                    ]
                                }
                            },
                    yaxis={'title': 'Weighted Price in USD'},
                    showlegend=True,
                    legend=go.layout.Legend(
                        # x=2,
                        # y=1.3,
                        xanchor="auto",
                        yanchor="auto"
                    ),
                    plot_bgcolor = 'rgb(229, 236, 246)',
                    # paper_bgcolor='rgb(50, 49, 53)',
                    # font= {
                    #     'color': 'rgb(255,255,255)',
                    #     'size': 12
                    # },
                    margin=go.layout.Margin(l=40, r=0, t=100, b=40)
                )
            },
        )  
        ], style={'margin': 0})
    ], className='detailed-graph')


# Callback for main Graph
@app.callback(
    Output('example-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):
    global data
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    '''
    TODO: Use pandas dataframe query here to get date range as per input.
    '''

    # p = ds.alldata()[(ds.alldata().index >=start_date) & (ds.alldata().index <=end_date)]
    return {
        'data' : [
            go.Scatter(
                x = data['Date'],
                y = data['Weighted_Price'],
                mode = 'lines',
                name= 'Weighted Price of all Crypto Currency',
            ),
            go.Scatter(
                x = data['Date'],
                y = data['Btc_Close_Price'],
                mode = 'lines',
                name= 'Closing Price of Bitcoin'
            ),
        ],
        'layout' : go.Layout(
            title='Different Crypto Currency Market Price VS BTC Closing Price',
            xaxis={'title': 'Time Period(Years)',
                    'type' : 'date',
                    'rangeslider': {'visible':True},
                    'rangeselector': {'visible':True, 
                        'buttons':
                            [
                                {'count':1,'step':'year','label':'1Y'},
                                {'count':5,'step':'year','label':'5Y'},
                                {'count':10,'step':'year','label':'10Y'},
                                {'step':'all','label':'Max'}
                            ]
                        }
                    },
            yaxis={'title': 'Weighted Price in USD'},
            showlegend=True,
            legend=go.layout.Legend(
                # x=2,
                # y=1.3,
                xanchor="auto",
                yanchor="auto"
            ),
            plot_bgcolor ='rgb(229, 236, 246)',
            # paper_bgcolor='rgb(50, 49, 53)',
            # font= {
            #     'color': 'rgb(255,255,255)',
            #     'size': 12
            # },
            margin=go.layout.Margin(l=40, r=0, t=100, b=40)
        )
    }


@app.callback(
    Output('download-button-container', 'children'),
    [Input('export-dropdown', 'value')])
def update_output(value):
    global data
    csv = data.to_csv(index =False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    filename = 'data.' + value
    # html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    path_to_file = 'data:text/csv;base64,' + payload
    return html.Div([
        html.A('Click here to download', href=path_to_file, download=filename)
    ], className='download-link')


def thumbnail_chart():
    g =  html.Div(
        children = [dcc.Graph(
            config={
            'displayModeBar': False
            },
            figure= {
                'data' : [
                    go.Scatter(
                        x = data['Date'],
                        y = data['Weighted_Price'],
                        mode = 'lines',
                        name= 'Weighted Price of all Crypto Currency',
                    ),
                    go.Scatter(
                        x = data['Date'],
                        y = data['Btc_Close_Price'],
                        mode = 'lines',
                        name= 'Closing Price of Bitcoin'
                    ),
                ],
                'layout' : go.Layout(
                    title='',
                    xaxis={'title': '',
                            'showticklabels':False
                            },
                    yaxis={'title': '','showticklabels':False},
                    showlegend=False,
                    # height = 90,
                    # width = 120,
                    plot_bgcolor='rgb(229, 236, 246)',
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0)
                )
            }
        ) 
    ], className='charts-thumbnail')
    return g


