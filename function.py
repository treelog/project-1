from utils import *

s_list = ['005930','000660', '074600', '007700', '014680', '074600.', '230360', '214150']

def get_current_ma(name):
    l, x = get_p_list(name, start_date='20160201', end_date='20201109')
    l, ma_240 = ma(l)
    x = x[239:]
    dr = derivative(ma_240)

    return l[-1], dr[-1]

def a(s_list):
