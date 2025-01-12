import datetime

import backtrader as bt

from backtrader_bokeh import bt
import inspect

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



cerebro = bt.Cerebro()



data = bt.feeds.YahooFinanceCSVData(
    dataname="datas/orcl-1995-2014.txt",
    # Do not pass values before this date
    fromdate=datetime.datetime(2000, 1, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2001, 2, 28),
    reverse=False,
    )
cerebro.adddata(data)

cerebro.run()

plot = bt.Bokeh()
cerebro.plot(plot, iplot=False)