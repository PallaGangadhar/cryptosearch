from data_store import process_and_get_crypto_data
from graph import load_main_chart


ALL_CHART_LIST = {
    'DCCMPvBCP': {
        'title': 'Different Crypto Currency Market Price VS BTC Closing Price',
        'x_label': '',
        'y_label': '',
        'data': {},
        'layout_opts': {}
    },
    'DCCMPvLCP': {
        'title': 'Different Crypto Currency Market Price VS LTC Closing Price',
        'x_label': '',
        'y_label': '',
        'data': {},
        'layout_opts': {}
    },
    'DCCMPvBCCP': {
        'title': 'Different Crypto Currency Market Price VS BTC-Cash Closing Price',
        'x_label': '',
        'y_label': '',
        'data': {},
        'layout_opts': {}
    },
}

def get_chart_layout(chart_url_id):
    pass


def load_chart_from_url(chart_url_id):
    '''
    Returns charts details using approriate chart_id according to requested URL
    '''
    chart_details = ALL_CHART_LIST.get(chart_url_id)

    if chart_details:
        data_df = process_and_get_crypto_data(chart_url_id)
        chart_details['data'] = data_df

        layout_opts = get_chart_layout(chart_url_id)
        chart_details['layout_opts'] = layout_opts

    else:
        default_chart = {}
        chart_details = default_chart

    chart_to_render = load_main_chart(chart_details)
    return chart_to_render
