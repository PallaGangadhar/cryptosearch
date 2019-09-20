'''
This module acts as data store for all the required data for the charts
and handles fetching the data/API calls and necessary processing.
'''
import pickle
import quandl
import pandas as pd
from db_exp import get_previous_data


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
    old_data = get_previous_data()

    BTC_URL = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190715&end=20500930"
    btc_df = get_CMC_data(BTC_URL)
    drop_cols = lambda df: df.drop(labels=['Open*', 'High', 'Low', 'Volume'], axis=1, inplace=True)
    drop_cols(btc_df)

    temp_df = old_data[['date', 'bitcoin_close', 'bitcoin_market_cap']]
    temp_df.rename(columns={'date':'Date', 'bitcoin_close':'Close**', 'bitcoin_market_cap': 'Market Cap'}, inplace=True)
    btc_df = btc_df.append(temp_df, ignore_index=True)
    btc_df.fillna(0, inplace=True)

    LTC_URL = "https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20190715&end=20500930"
    ltc_df = get_CMC_data(LTC_URL)
    drop_cols(ltc_df)

    temp_df = old_data[['date', 'litcoin_close', 'litcoin_market_cap']]
    temp_df.rename(columns={'date':'Date', 'litcoin_close':'Close**', 'litcoin_market_cap': 'Market Cap'}, inplace=True)
    ltc_df = ltc_df.append(temp_df, ignore_index=True)
    ltc_df.fillna(0, inplace=True)
    
    BTC_CASH_URL = "https://coinmarketcap.com/currencies/bitcoin-cash/historical-data/?start=20190715&end=20500930"
    btc_cash_df = get_CMC_data(BTC_CASH_URL)
    drop_cols(btc_cash_df)

    temp_df = old_data[['date', 'bitcoincash_close', 'bitcoincash_market_cap']]
    temp_df.rename(columns={'date':'Date', 'bitcoincash_close':'Close**', 'bitcoincash_market_cap': 'Market Cap'}, inplace=True)
    btc_cash_df = btc_cash_df.append(temp_df, ignore_index=True)
    btc_cash_df['Market Cap'].fillna(0, inplace=True)
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
    resultant_df.set_index('Date', inplace=True)

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

    intersected_df = pd.merge(sov_index_df, gold_df, on='Date', how='inner', left_index=True)
    intersected_df['SOV_index'] = intersected_df['SOV_index'].multiply(100)
    intersected_df['Value'] = intersected_df['Value'].multiply(100)
    intersected_df['Rolling_corr'] = intersected_df['SOV_index'].rolling(30).corr(intersected_df['Value'])
    intersected_df.set_index('Date', inplace=True)
    
    return intersected_df


############### for graph_three.py ###############
def get_graph_three_data():
    pass


if __name__ == '__main__':
    pass