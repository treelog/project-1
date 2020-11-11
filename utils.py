import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock


def smooth(l, weight):
    s = np.zeros(len(l))
    s[0] = l[0]
    for i in range(1, len(l)):
        s[i] = s[i - 1] * (1 - weight) + l[i] * (weight)
    return s


def double_smooth(l, alpha, beta):
    s = np.zeros(len(l))
    b = np.zeros(len(l))
    s[0] = l[0]
    b[0] = l[1] - l[0]
    for i in range(1, len(l)):
        s[i] = alpha * l[i] + (1 - alpha) * (s[i - 1] + b[i - 1])
        b[i] = beta * (s[i] - s[i - 1]) + (1 - beta) * b[i - 1]
    return s


def derivative(l):
    d = np.zeros(len(l))
    for i in range(1, len(l)):
        d[i] = (l[i] - l[i - 1]) / l[i]
    return d


def derivative2(l, s):
    d = np.zeros(len(l))
    for i in range(0, len(l)):
        d[i] = (s[i] - l[i])
    return d


def ma(l, k=240):
    ma = []
    for i in range(k - 1, len(l)):
        ma.append(np.mean(l[i - k + 1:i]))

    return l[k - 1:], ma

def draw(s_list, start_date='20160201', end_date='20201109'):
    for name in s_list:
        print(stock.get_market_ticker_name(name[:-3]))
        s = pd.DataFrame()
        start_date = str(int(start_date)-10000)
        s_ = stock.get_market_ohlcv_by_date("20160201", "20201109", name[:-3])
        l = list(s_['종가'])
        x = list(s_.index)

        #smoothed = double_smooth(l, 0.02, 0.03)
        l, ma_240 = ma(l)
        x = x[239:]
        #print(ma_240)
        dr = double_smooth(derivative(ma_240), 0.03, 0.03)
        plt.figure(figsize=(10,10))
        plt.plot(x, ma_240)
        plt.plot(x, l)
        plt.show()
        #plt.figure(figsize=(10,10))
        plt.plot(x, dr)
        plt.plot(x, np.zeros(len(dr)))
        #plt.yscale('log')
        plt.show()