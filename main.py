import utils
import function
from datetime import date, timedelta
from pykrx import stock
#def main():


if __name__=='__main__':
    s_list = ['005930', '000660', '074600', '007700', '014680', '074600', '230360', '214150']
    s_list_2 = ['AAPL', 'AMZN', 'NVDA', 'GOOGL', 'SBUX', 'FB', 'NFLX', 'O']
    s_list_3 = ['119860', '214150', '230360', '067900', '102710', '051160', '139670', '033290']
    #function.current_ma_dr(s_list_2, country='us')
    #function.backtest('GOOG', country='us')
    #function.backtest('007700', country='kr')
    #for name in s_list_2:
    #    function.backtest(name, country='us')
    #for name in s_list:
    #    function.backtest(name, country='kr')
    start_date = '20171010'
    end_date = '20201109'
    for name in s_list_3:
        # try:
        print(stock.get_market_ticker_name(name))
        good_list, bad_list = function.backtest(name,
                                                date(int(start_date[:4]), int(start_date[4:6]), int(start_date[6:8])),
                                                date(int(end_date[:4]), int(end_date[4:6]), int(end_date[6:8])),
                                                country='kr')
