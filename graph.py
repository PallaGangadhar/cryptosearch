
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from data_store import process_and_get_crypto_data
from app import app


data = process_and_get_crypto_data()
x_axis_period = data['Date']
y_axis_weighted_prc = data['weighted_price']
y_axis_btc_close = data['btc_close_prc']


def load_main_chart():
    return html.Div(children=[
        # html.H3(children='BTC Exchange Analysis from 2014 to 2019'),
        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                start_date=x_axis_period.min(),
                end_date=x_axis_period.max(),
                max_date_allowed=x_axis_period.max(),
            ),
        ], style={'margin-left':'70%'}),
        
        html.Div([
            dcc.Graph(
            id='example-graph',
            figure= {
                'data' : [
                        go.Scatter(
                            x = x_axis_period,
                            y = y_axis_weighted_prc,
                            mode = 'lines'
                        ),
                        go.Scatter(
                            x = x_axis_period,
                            y = y_axis_btc_close,
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
                        x=0,
                        y=1
                    ),
                    plot_bgcolor = 'rgb(229, 236, 246)',
                    margin=go.layout.Margin(l=40, r=0, t=100, b=40)
                )
            },
        )  
        ], style={'margin': '50px'})
    ], className='detailed-graph')


# Callback for main Graph
@app.callback(
    Output('example-graph', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')])
def update_output(start_date, end_date):

    updated_range = x_axis_period[(x_axis_period >= start_date) & (x_axis_period <= end_date)]
    '''
    TODO: Use pandas dataframe query here to get date range as per input.
    '''

    # p = ds.alldata()[(ds.alldata().index >=start_date) & (ds.alldata().index <=end_date)]
    return {
        'data' : [
            go.Scatter(
                x = updated_range,
                y = y_axis_weighted_prc,
                mode = 'lines',
                name= 'Weighted Price of all Crypto Currency',
            ),
            go.Scatter(
                x = updated_range,
                y = y_axis_btc_close,
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
                x=0,
                y=1
            ),
            plot_bgcolor = 'rgb(229, 236, 246)',
            margin=go.layout.Margin(l=40, r=0, t=100, b=40)
        )
    }

    
def thumbnail_chart():
    g =  html.Div(
        children = [dcc.Graph(
            config={
            'displayModeBar': False
            },
            figure= {
                'data' : [
                    go.Scatter(
                        x = x_axis_period,
                        y = y_axis_weighted_prc,
                        mode = 'lines',
                        name= 'Weighted Price of all Crypto Currency',
                    ),
                    go.Scatter(
                        x = x_axis_period,
                        y = y_axis_btc_close,
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
                    height = 90,
                    width = 120,
                    plot_bgcolor = 'rgb(229, 236, 246)',
                    margin=go.layout.Margin(l=0, r=50, t=10, b=40)
                    
                )
            }
        ) 
    ], className='charts-thumbnail')
    return g
    
