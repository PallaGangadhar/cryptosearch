'''
This module acts as data store for all the required data for the charts
and handles fetching the data/API calls and necessary processing.
'''
import pickle
import quandl
import pandas as pd


QUANDLE_DATA = {}
BTC_QUANDL_CODE = "BCHAIN/MKPRU"

# Using a helper function to download and cache datasets from Quandl
def get_quandl_data(quandl_id):
    '''Download and cache Quandl dataseries'''
    cache_path = '{}.pkl'.format(quandl_id).replace('/', '-')
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)
        print('Loaded {} from cache'.format(quandl_id))
    except (OSError, IOError) as e:
        print('Downloading {} from Quandl'.format(quandl_id))
        quandl.ApiConfig.api_key = "wRpgyxQ_ACxuvoF7BAys"
        df = quandl.get(quandl_id, returns="pandas")
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(quandl_id, cache_path))
    return df


def get_btc_data():
    global BTC_QUANDL_CODE
    response_df = get_quandl_data(BTC_QUANDL_CODE)

    time_period = response_df.index
    market_price_value = response_df['Value']

    return {'x_time_range':  time_period, 'y_value': market_price_value}


# CoinMarketCap API call
def get_CMC_data(data_api_url):
    '''
    API call to CoinMarketCap which return pandas dataframe object
    for the given url
    ARGS:
    data_api_url - str: CoinMarketCap API URL
    '''
    api_data = pd.read_html(data_api_url)
    df = api_data[0]

    # return df
    return df.head(737)


def process_and_get_crypto_data():

    BTC_URL = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20500930"
    btc_df = get_CMC_data(BTC_URL)
    drop_cols = lambda df: df.drop(labels=['Open*', 'High', 'Low', 'Volume'], axis=1, inplace=True)
    drop_cols(btc_df)

    LTC_URL = "https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20130428&end=20500930"
    ltc_df = get_CMC_data(LTC_URL)
    drop_cols(ltc_df)

    BTC_CASH_URL = "https://coinmarketcap.com/currencies/bitcoin-cash/historical-data/?start=20130428&end=20500930"
    btc_cash_df = get_CMC_data(BTC_CASH_URL)
    drop_cols(btc_cash_df)
    btc_cash_df['Market Cap'] = btc_cash_df['Market Cap'].astype(int)

    # calculate Total Market Capital of Bitcoin, Litecoin and Bitcoin Cash
    total_market_cap = btc_df['Market Cap'] + \
        ltc_df['Market Cap'] + btc_cash_df['Market Cap']

    # calulate Total Weighted Price of those 3
    for_wp = lambda df: df['Close**'] * df['Market Cap']
    for_btc_wp = for_wp(btc_df)
    print("for_type:", for_btc_wp)
    for_ltc_wp = for_wp(ltc_df)
    for_btc_cash_wp = for_wp(btc_cash_df)

    weighted_price = (for_btc_wp + for_ltc_wp +
                      for_btc_cash_wp)/total_market_cap

    btc_df['Date'] = pd.to_datetime(btc_df['Date'])
    resultant_df = pd.DataFrame({'Date': btc_df['Date'], 'Weighted_Price': weighted_price, 'Btc_Close_Price': btc_df['Close**']})

    return resultant_df
