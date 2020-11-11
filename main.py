import utils
import function

#def main():


if __name__=='__main__':
    s_list = ['005930', '000660', '074600', '007700', '014680', '074600', '230360', '214150']
    s_list_2 = ['AAPL', 'AMZN', 'NVDA', 'GOOGL', 'SBUX', 'FB', 'NFLX', 'O']
    #function.current_ma_dr(s_list_2, country='us')
    function.backtest('AAPL', country='us')
    #for name in s_list_2:
    #    function.backtest(name, country='us')
    #for name in s_list:
    #    function.backtest(name, country='kr')

