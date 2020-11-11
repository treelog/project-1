import numpy as np
from utils import *

def get_current_ma(name, k=240):
    l, x = get_p_list(name, start_date='20160201', end_date='20201109')
    l, ma_240 = ma(l, k)
    x = x[239:]
    dr = derivative(ma_240)

    return l, ma_240, dr

def annualized(i):
    return (1+i)**240-1

def criteria(p, ma, dr):
    discripency_rate_cr = (p[-1]-ma[-1])/ma[-1]
    annualized_growth_rate = (1+dr[-1])**240-1
    print(discripency_rate_cr)
    print(annualized_growth_rate)
    if discripency_rate_cr <0.2 and annualized_growth_rate > -0.1:
        return True
    else:
        return False

def criteria2(p, ma, dr):
    discripency_rate_cr = (p[-1]-ma[-1])/ma[-1]
    annualized_growth_rate_list = np.array([(1+dr[i])**240-1 for i in range(len(dr)-5, len(dr))])
    #print(discripency_rate_cr)
    print(annualized_growth_rate_list)
    if annualized_growth_rate_list[-1] > 0 and np.array([annualized_growth_rate_list>-0.1]).all() \
            and np.array([annualized_growth_rate_list<0.1]).all():
        return True
    else:
        return False

def current_ma_dr(s_list):
    for name in s_list:
        p, ma, dr = get_current_ma(name)
        print(name)
        #print((p[-1]-ma[-1])/ma[-1])
        #print((1+dr[-1])**240-1)
        if criteria2(p, ma, dr):
            print('Good')
        else:
            #print(stock.get_market_ticker_name(name))
            print('Bad')

