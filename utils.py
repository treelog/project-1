import pandas as pd
import yfinance as yf
import datetime
import time
import requests
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock

def annualized(i):
    return (1+i)**240-1

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

def derivative_abs(l):
    d = np.zeros(len(l))
    for i in range(1, len(l)):
        d[i] = (l[i] - l[i - 1])
    return d

def ma(l, start_index=0, k=240):
    ma = []
    for i in range(len(l)):
        if i >= k - 1:
            ma.append(np.mean(l[i - k + 1:i]))
        else:
            ma.append(np.mean(l[:k]))
    #print(ma[start_index:])

    return ma[start_index:]

def get_p_list_kr(name, start_date, end_date):
    #print(start_date)
    start_date = str(int(start_date) - 20000)
    s_ = stock.get_market_ohlcv_by_date(start_date, end_date, name)
    l = list(s_['종가'])
    x = list(s_.index)
    #print(x)
    start_index = x.index(datetime.datetime(int(start_date[:4])+1, int(start_date[4:6]), int(start_date[6:8])))

    return l, x, start_index

def get_p_list_us(name, start_date, end_date):
    start = datetime.datetime(int(start_date[:4])-2, int(start_date[4:6]), int(start_date[6:8]))
    end = datetime.datetime(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8]))
    s_ = yf.download(name, start=start, end=end, progress=False)
    l = list(s_['Adj Close'])
    x = list(s_.index)
    start_index = x.index(datetime.datetime(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:8])))

    return l, x, start_index

def draw(s_list, start_date='20160201', end_date='20201109'):
    for name in s_list:
        l, x, start_index = get_p_list_kr(name, start_date, end_date)

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

