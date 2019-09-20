import pymysql
import pandas as pd
from sqlalchemy import create_engine


def get_previous_data():


    try:
        db_connection_str = 'mysql+pymysql://root@localhost/crypto_research'
        columnname = ['date','bitcoin_close','bitcoin_market_cap','litcoin_close','litcoin_market_cap','bitcoincash_close','bitcoincash_market_cap']
        df1 = pd.read_csv('b1.csv',header=20,usecols=(0,3,4,5,6,7,8),names=columnname, thousands=',')

        db_connection = create_engine(db_connection_str)
        frame   = df.to_sql('bitcoin1', db_connection, if_exists='replace')
    except Exception as e:
        print('Database connection error occured:', e)

    try:
        df = pd.read_sql('SELECT * FROM bitcoin1', con=db_connection)

    except Exception as e:
        print("Error while reading data from database to dataframe.", e)

    return df
