import os
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mpl_dates
import yfinance as yf


""" Clears console """
clear_console = lambda : os.system('cls||clear')

""" Checks if file already exists """
file_exist = lambda x : os.path.isfile(x)

""" Returns a concatenated string from two inputs """
title_str = lambda x, y : str(x) + str(y)

""" Returns a data frame with the absolute spread between two columns """
spread = lambda x : pd.DataFrame(abs(x.iloc[:,0] - x.iloc[:,1]))

""" Simple moving average """
sma = lambda src, len : src.rolling(len).mean()

""" Exponential moving average """
ema = lambda src, len : round(src.iloc[:,4].ewm(span=len, adjust=False).mean(), 2)


def gather_data(ticker, start, end, ext='.txt', data_dir='data\\'):
    """
    Gathers data from yahoo servers
    or reads it from local source
    and returns the time frame asked
        ticker: Ticker symbol
        start: Starting datetime object
        end: Ending datetime object
        ext: File extension to save data file
        data_dir: Directory to save data file
    """
    f = data_dir + ticker + ext
    if file_exist(f):
        df = pd.read_csv(f, parse_dates=True, header=0, index_col=0)
    else:
        yf.pdr_override()
        df = pdr.get_data_yahoo(ticker)
        df.to_csv(f)
    tf = df.loc[start:end][:]
    del df
    return tf


# class candlestick_plot():
#     """
#     Candlestick plot object.
#     It gathers the time framed data request
#         ticker: Ticker symbol
#         start: Starting datetime object
#         end: Ending datetime object
#     """
#     def __init__(self, ticker, start, end):
#         plt.style.use('ggplot')
#         data = gather_data(ticker, start, end)
#         data = data.rename_axis('Date').reset_index()
#         ohlc = data.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
#         self.data = ohlc[:]
#         ohlc['Date'] = pd.to_datetime(ohlc['Date'])
#         ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
#         ohlc = ohlc.astype(float)

#         self.fig, self.ax = plt.subplots()

#         candlestick_ohlc(self.ax,
#                         ohlc.values,
#                         width=0.6,
#                         colorup='green',
#                         colordown='red'
#                         )

#         self.ax.set_xlabel('Date')
#         self.ax.set_ylabel('Price')
#         self.fig.suptitle(ticker)

#         date_format = mpl_dates.DateFormatter('%d-%m-%Y')
#         self.ax.xaxis.set_major_formatter(date_format)
#         self.fig.autofmt_xdate()

#         del data


#     def show(self):
#         plt.show()


def print_statement(*args):
    """
    Prints the backtest final
    statement with arguments given

        Order:
        0   ticker,
        1   start,
        2   end,
        3   sample size,
        4   emas used,
        5   batting avg,
        6   ratios,
        7   avg_gain,
        8   avg_loss,
        9   max_gain,
        0   max_loss,
        11  number of trades,
        12  total return %,
        13  buy and hold return %,
        14  buy and hold entry price,
        15  buy and hold closing price
    """
    clear_console()
    print(
    """
    \n
    Results for {}

    Time frame: {} to {}
    Sample size: {}
    EMAs used: {}

    Batting Avg: {}
    Gain/Loss ratio: {}
    Average gain: {}
    Average loss: {}
    Max return: {}
    Max loss: {}
    Total return over {} trades: {}%

    Buy and hold return: {}%
    Buy and hold entry price: {}
    Buy and hold closing price: {}
    \n
    """.format(
        *args
        )
    )