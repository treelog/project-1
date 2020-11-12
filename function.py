import numpy as np
from datetime import date, timedelta
from utils import *

def get_current_ma(name, country, start_date='20160201', end_date='20201109', k=240):
    if country=='kr':
        l, x = get_p_list_kr(name, start_date=start_date, end_date=end_date)
    elif country == 'us':
        l, x = get_p_list_us(name, start_date=start_date, end_date=end_date)

    l, ma_240 = ma(l, k)
    x = x[239:]
    dr = derivative(ma_240)

    return l, ma_240, dr

def criteria(p, ma_low, dr):
    discripency_rate_cr = (p[-1]-ma_low[-1])/ma_low[-1]
    annualized_growth_rate = (1+dr[-1])**240-1
    dr = ma(derivative(ma_low),0, k=60)
    dr = derivative_abs(dr)
    #print(discripency_rate_cr)
    #print(annualized_growth_rate)
    #(len(p)>1 and (p[-1] - p[-2])/p[-2]>0.05)
    if (discripency_rate_cr <annualized_growth_rate*1/4 and annualized_growth_rate > 0) :
        return True
    else:
        return False

def criteria1(p, ma, dr):
    discripency_rate_cr = (p[-1]-ma[-1])/ma[-1]
    annualized_growth_rate = (1+dr[-1])**240-1
    #print(discripency_rate_cr)
    #print(annualized_growth_rate)
    #(len(p)>1 and (p[-1] - p[-2])/p[-2]>0.05)
    if annualized_growth_rate > 0:
        return True
    else:
        return False

def criteria2(p, ma, dr):
    discripency_rate_cr = (p[-1]-ma[-1])/ma[-1]
    annualized_growth_rate_list = np.array([(1+dr[i])**240-1 for i in range(len(dr)-5, len(dr))])
    #print(discripency_rate_cr)
    #print(annualized_growth_rate_list)
    if annualized_growth_rate_list[-1] > 0 and np.array([annualized_growth_rate_list>-0.1]).all() \
              and np.array([annualized_growth_rate_list<0.1]).all():
        return True
    else:
        return False

def criteria3(p, ma_high_freq, ma_low_freq, dr):
    discripency_rate_cr = (p[-1] - ma_low_freq[-1]) / ma_low_freq[-1]
    annualized_growth_rate = (1+dr[-1])**240-1
    if p[-1]<ma_high_freq[-1]*0.95 and discripency_rate_cr>0.4:
        return True
    else:
        return False

def current_ma_dr(s_list, country='kr'):
    for name in s_list:
        p, ma, dr = get_current_ma(name, country)
        print(name)
        #print((p[-1]-ma[-1])/ma[-1])
        #print((1+dr[-1])**240-1)
        if criteria2(p, ma, dr):
            print('Good')
        else:
            #print(stock.get_market_ticker_name(name))
            print('Bad')


def backtest(name, start=date(2013, 8, 14), end=date(2020, 11, 11), country='kr'):
    budget = 100
    no_share = 0
    bs = 0 # if bs = 0: sell, bs = 1: buy
    holding_period = 0
    bad_list = []
    good_list = []
    backtest_start = start
    backtest_end = end

    end_date = str(backtest_end).replace('-', '')
    start_date = str(backtest_start).replace('-', '')

    if country == 'kr':
        l, x, start_index = get_p_list_kr(name, start_date=start_date, end_date=end_date)
    elif country == 'us':
        l, x , start_index = get_p_list_us(name, start_date=start_date, end_date=end_date)

    p = l[start_index:]
    ma_240 = ma(l, start_index, 240)
    ma_60 = ma(l, start_index, 20)
    dr = derivative(ma_240)
    x = x[start_index:]

    for i in range(1, len(p)):
        if bs == 1:
            holding_period += 1
        if criteria(p[:i], ma_240[:i], dr[:i]):
            #print('Good', p[i-1], x[i-1])
            good_list.append(x[i-1])
            if bs == 0:
                no_share = budget/p[i-1]
                budget = 0
                bs = 1
        elif  criteria1(p[:i], ma_240[:i], dr[:i]) and bs==0:
            #print('Good', p[i-1], x[i-1])
            no_share = budget/p[i-1]
            budget = 0
            bs = 1
        elif criteria3(p[:i], ma_60[:i], ma_240[:i], dr[:i]):
            #print('Bad', p[i-1], x[i-1])
            bad_list.append(x[i-1])
            if bs==1:
                budget = no_share*p[i-1]
                no_share = 0
                bs = 0

    if budget ==0:
        budget = no_share*p[-1]
    print(name)
    print('Algorithm Performance:', budget, 'Holding Period', holding_period)
    print('Buy and Hold:', 100*(p[-1]/p[0]), 'Holding Period', len(p)-4)
    return good_list, bad_list