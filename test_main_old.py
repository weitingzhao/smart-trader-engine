from __future__ import (
    absolute_import, division, print_function,unicode_literals
)
import json
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
from bokeh.model import Model

import backtrader as bt
from backtrader_plotting import Bokeh,OptBrowser
from backtrader_plotting.bokeh import BokehWebapp
from backtrader_plotting.schemes import Tradimo
from cerebro.ray_strategy import RayStrategyProfile
from strategy.strategy1stoperation import Strategy1stOperation

def test_main():
    # Create a cerebro entity
    cerebro = bt.Cerebro()


    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'datas/orcl-1995-2014.txt')
    # Create a Data Feed
    data = bt.feeds.YahooFinanceCSVData(
        dataname=datapath,
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2000, 12, 31),
        reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)
    # Set our desired cash start
    cerebro.broker.setcash(1000.0)
    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # Set the Commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.001)



    # Add a strategy
    strats = cerebro.addstrategy(Strategy1stOperation)
    # strats = cerebro.addstrategy(BollingerBifrostStrategy)

    # Optimize the strategy
    # strats = cerebro.optstrategy(TestStrategy, map_period=range(10, 31))
    # cerebro.addanalyzer(AnnualReturn, _name='annual_return')
    # cerebro.addanalyzer(SQN, _name='sqn')
    # # cerebro.addanalyzer(TimeReturn, _name='time_return')
    # cerebro.addanalyzer(SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days)
    # cerebro.addanalyzer(TradeAnalyzer, _name='trade_analyzer')


    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    # Run over everything
    results = cerebro.run()
    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # A. For Add Strategy
    # cerebro.plot()

    bo = Bokeh(style='bar', plot_mode='single', scheme=Tradimo(), output_mode='show') # tabs = 'multi',
    cerebro.plot(bo)

    # # B. For Add Strategy
    # b = Bokeh(style='bar', scheme=Tradimo())
    # browser = OptBrowser(b, results)
    # browser.start()


    # # Extract data into a list
    # data_list = []
    # for i in range(len(data.datetime.array)):
    #     data_list.append([
    #         data.datetime.date(-i),
    #         data.open[-i],
    #         data.high[-i],
    #         data.low[-i],
    #         data.close[-i],
    #         data.volume[-i],
    #         data.adjclose[-i]
    #     ])
    #
    # # Convert the list to a DataFrame
    # df = pd.DataFrame(data_list, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'])
    #
    # # Display the first few rows of the DataFrame
    # print(df.head())


if __name__ == '__main__':
    test_main()