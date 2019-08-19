import base64
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from data_store import process_and_get_crypto_data
from app import app


data = process_and_get_crypto_data()

main_graph_layout = go.Layout(
    title='Different Crypto Currency Market Price VS BTC Closing Price',
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
                    ],
                    value='',
                    style={'width': 200}
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
    return {
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
                name='Closing Price of Bitcoin'
            ),
        ], 'layout': main_graph_layout}


@app.callback(
    Output('download-button-container', 'children'),
    [Input('export-dropdown', 'value')])
def update_download_data(value):
    global data
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    filename = 'data.' + value
    path_to_file = 'data:text/csv;base64,' + payload
    return html.Div([
        html.A('Click here to download CSV',
               href=path_to_file, download=filename)
    ], className='download-link')


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
                        name='Closing Price of Bitcoin'
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
