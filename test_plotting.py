from __future__ import (
    absolute_import, division, print_function,unicode_literals
)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
import pandas as pd

from backtrader_plotting import Bokeh,OptBrowser
from backtrader_plotting.schemes import Tradimo

class TestStrategy(bt.Strategy):
    params = (
        ('buydate', 21),
        ('holdtime', 6),
    )

    def next(self):
        if len(self.data) == self.p.buydate:
            self.buy(self.datas[0], size=None)

        if len(self.data) == self.p.buydate + self.p.holdtime:
            self.sell(self.datas[0], size=None)


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    # cerebro.addstrategy(TestStrategy, buydate=3)
    cerebro.optstrategy(TestStrategy, buydate=range(1,10,1))

    cerebro.addanalyzer(bt.analyzers.SharpeRatio)

    data = bt.feeds.YahooFinanceCSVData(
        dataname="datas/orcl-1995-2014.txt",
        # Do not pass values before this date
        fromdate=datetime.datetime(2000, 1, 1),
        # Do not pass values after this date
        todate=datetime.datetime(2001, 2, 28),
        reverse=False,
        )
    cerebro.adddata(data)

    results =  cerebro.run(optreturn=True)

    b = Bokeh(style='bar', scheme=Tradimo())
    browser = OptBrowser(b, results)
    browser.start()

