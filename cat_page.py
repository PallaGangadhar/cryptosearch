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


dashboard_title = html.Div([
        html.H3(children='Crypto Dashboard', className='dashboard-title')
    ]
),

cat_tabs = html.Div(id='categoryMenu',
    children=[
        html.Div(
            html.H2(children='Crypto Dashboard'),
            className='dashboard-title'
        ),        
        dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='At a glance', value='tab-1'),
                dcc.Tab(label='Popular Series', value='tab-2'),
                dcc.Tab(label='Popular Categories', value='tab-3'),
                dcc.Tab(label='Recent Series', value='tab-4'),
            ]
        ),
        html.Div(id='tabs-content')
    ], 
    className="category-tabs"
)


# Dashboard Index Page
tab_one_content = html.Div([
    html.Div([
        html.Div([
            html.Ul([
                html.Li([
                    dcc.Link('Different Crypto Currency Market Price VS BTC Closing Price', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Sample chart two', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Another sample chart', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Sample BTC vs LTC Market Price', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                
            ],style={'text-decoration': 'none','font-size':'18px','list-style-type':'none','font-weight':'300'},className='ten columns'),
            
            html.Div([
                thumbnail_chart()
                # html.H4('hello'),
            ],style={'margin-top':'1%'},className='two columns'),
            html.Div([
                thumbnail_chart()
            ],style={'margin-top':'1%'},className='two columns'),
            html.Div([
                thumbnail_chart()
            ],style={'margin-top':'1%'},className='two columns'),
        ],className='six columns'),

        html.Div([
            html.Ul([
                html.Li([
                    dcc.Link('Different Crypto Currency Market Price VS BTC Closing Price', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Sample chart two', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Another sample chart', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                html.Li([
                    dcc.Link('Sample BTC vs LTC Market Price', href = '/graph',style={'text-decoration': 'none'}),
                ],style={'margin-top':'3%'}),

                
            ],style={'text-decoration': 'none','font-size':'18px','list-style-type':'none','font-weight':'300'},className='ten columns'),
            
            html.Div([
                thumbnail_chart()
                # html.H4('hello'),
            ],style={'margin-top':'1%'},className='two columns'),
            html.Div([
                thumbnail_chart()
            ],style={'margin-top':'1%'},className='two columns'),
            html.Div([
                thumbnail_chart()
            ],style={'margin-top':'1%'},className='two columns'),
        ],className='six columns'),
        
    ],className='row',style={'margin-left':'2%'}),
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab_one_content
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Popular Series')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Popular Categories')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Recent Series')
        ])