# first thing we need to do is install yfinance (pandas_datareader)
# pip install yfinance

import pandas as pd
import yfinance as yf
import os
import datetime
import time

# import all of the relevenat paths/ libraries that we will need


def get_earliest_date(tickers):
    stock = yf.Ticker(tickers)
    history = stock.history(period="max")
    if not history.empty:
        earliest_date = history.index[0].strftime('%Y-%m-%d')
        return earliest_date
    else:
        return None

def download_data(tickers, start, end, all_data=False): # if set to be true then it would download all of the data (1970 - present day)

    count = 1
    if all_data==True:
        end = datetime.datetime.now()
        end = '%s-%s-%s' % (end.month, end.day, end.year)
        start = '01-01-1970'

    directory = 'stock_data'
    if not os.path.exists(directory):
        os.makedirs(directory) # creating a directory (file name will be ---)

    d = {}
    for ticker in tickers:
        filename = directory+'/'+ticker+'.csv'
        d[ticker] = yf.download(ticker, start, end)

        if d[ticker].empty:
            d[ticker] = yf.download(ticker, '2002-01-01', end)

        d[ticker].to_csv(filename)
        count = count + 1
        if count % 50 == 0:
            time.sleep(10) # essential for not having ip address blocked by yahoo finance

    return

if __name__ == '__main__':

    tickers_df = pd.read_csv('ZZS&P500symbols.csv')
    tickers = tickers_df['Ticker'].tolist()

    # start = '1970-01-01'
    start = '2023-07-01'
    end = datetime.datetime.now().strftime('%Y-%m-%d')  # Get current date in YYYY-MM-DD format
    download_data(tickers, start, end)

# now we have all of the data for our stocks in csv files formated as: TICKER.csv inside of stock_data folder
