'''
This module acts as data store for all the required data for the charts
and handles fetching the data/API calls and necessary processing.
'''
import pickle
import quandl
import pandas as pd


BTC_QUANDL_CODE = "BCHAIN/MKPRU"
# https://www.quandl.com/data/BCHAIN/MKPRU-Bitcoin-Market-Price-USD

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

############### for graph.py ###############
# CoinMarketCap API call for graph.py
def get_CMC_data(data_api_url):
    '''
    API call to CoinMarketCap which return pandas dataframe object
    for the given url
    ARGS:
    data_api_url - str: CoinMarketCap API URL
    '''
    api_data = pd.read_html(data_api_url)
    df = api_data[0]

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

    for_ltc_wp = for_wp(ltc_df)
    for_btc_cash_wp = for_wp(btc_cash_df)

    # Calculation of Store of Store of Value Index
    sov_index = (for_btc_wp + for_ltc_wp +
                      for_btc_cash_wp)/total_market_cap

    btc_df['Date'] = pd.to_datetime(btc_df['Date'])
    resultant_df = pd.DataFrame({'Date': btc_df['Date'], 'SOV_index': sov_index, 'Btc_Close_Price': btc_df['Close**']})

    return resultant_df


############### for graph_two.py ###############
def get_graph_two_data():
    # https://www.quandl.com/data/WGC/GOLD_DAILY_USD-Gold-Prices-Daily-Currency-USD
    AU_QUANDL_CODE = "WGC/GOLD_DAILY_USD"
    gold_df = get_quandl_data(AU_QUANDL_CODE)
    gold_df['Value'] = gold_df['Value'].pct_change(periods=2)
    gold_df.reset_index(level=0, inplace=True)

    sov_index_df = process_and_get_crypto_data()
    sov_index_df['SOV_index'] = sov_index_df['SOV_index'].pct_change(periods=2)
    sov_index_df.drop('Btc_Close_Price', axis=1, inplace=True)

    intersected_df = pd.merge(sov_index_df, gold_df, how='inner')
    intersected_df['SOV_index'] = intersected_df['SOV_index'].multiply(100)
    intersected_df['Value'] = intersected_df['Value'].multiply(100)
    intersected_df['Rolling_corr'] = intersected_df['SOV_index'].rolling(30).corr(intersected_df['Value'])

    return intersected_df


# if __name__ == '__main__':
#     sov_index_df = process_and_get_crypto_data()
#     sov_index_df['SOV_index'] = sov_index_df['SOV_index'].pct_change(periods=2)
#     sov_index_df.drop('Btc_Close_Price', axis=1, inplace=True)

#     gold_df = get_quandl_data(AU_QUANDL_CODE)
#     gold_df['Value'] = gold_df['Value'].pct_change(periods=2)
#     gold_df.reset_index(level=0, inplace=True)

#     intersected_df = pd.merge(sov_index_df, gold_df, how='inner')
#     intersected_df['SOV_index'] = intersected_df['SOV_index'].multiply(100)
#     intersected_df['Value'] = intersected_df['Value'].multiply(100)

#     intersected_df['Rolling_corr'] = intersected_df['SOV_index'].rolling(30).corr(intersected_df['Value'])

#     print(intersected_df.info())
#     print(intersected_df.head())
#     print(intersected_df.tail())