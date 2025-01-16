import logging
import backtrader as bt
from strategy.indicator.bollinger_smoother_3bands import BollingerSmoother3bands
from strategy.indicator.macd_histo_custom import CustomMACDHisto
from strategy.indicator.macd_mtf import MACD_MTF
from strategy.indicator.rs_bands import SupportResistanceBands
from strategy.indicator.support_resistance_channels import SupportResistanceChannels


# Create a Stratey
class Strategy1stOperation(bt.Strategy):
    params = (
        # Nadaraya smoothed Bollinger Bands
        ('map_period', 10),
        ('printlog', True),
        ('atr_period', 14),

        ('buy_delta', 0.50),
        ('sell_delta', 0.50),

        # Support Resistance Channels
        ('sr_period', 20),
        ('channel_width', 5),
        ('min_strength', 1),
        ('max_num_sr', 6),
        ('loopback', 290),

        # MACD
        ('fast_length', 12),
        ('slow_length', 26),
        ('signal_length', 9),
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))
            logging.log(logging.INFO, txt)  # Log to console


    def __init__(self):
        self.plot_objects = None  # Initialize plot_objects to store plot references

        # Keep a reference to the "close" line in the data[0] dataseries
        self.data_close = self.datas[0].close

        # To keep track of pending orders
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.bar_executed = 0

        # Part 1. Indicators
        # Nadaraya smoothed flux charts with three different bands
        self.bbands = BollingerSmoother3bands(self.data)
        # Add MACD
        self.macd = CustomMACDHisto(
            self.data,
            period_me1=self.p.fast_length, #12
            period_me2=self.p.slow_length, #26
            period_signal=self.p.signal_length #6
        )

        # self.macd = MACD_MTF(self.data)
        # Add ATR
        self.atr = bt.indicators.ATR(self.data, period=self.p.atr_period) # plot=False
        # Add Support Resistance Channels
        self.sr_v2 = SupportResistanceChannels(self.data, period=self.p.sr_period)
        self.srchannels = SupportResistanceBands(
            self.data,
            period=self.p.sr_period,
            channel_width=self.p.channel_width,
            min_strength=self.p.min_strength,
            max_num_sr=self.p.max_num_sr,
            loopback=self.p.loopback
        )


        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.RSI(self.datas[0])
        # bt.indicators.ATR(self.datas[0], plot=False)


    def next(self):
        # self.log('NEXT %s => Close %.2f' % (self.datas[0].datetime.datetime(0).isoformat(), self.data_close[0]))
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            buy_compound = self.bbands.bold_1[0] + (self.p.buy_delta * self.atr[0])
            # Not yet ... we MIGHT BUY if ...
            if self.data_close[0] < buy_compound:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log(
                    'BUY CREATE %s (Close) %.2f < (Compound) %.2f :[BB_Low+(ATR * Buy delta) %.2f + %.2f * %.2f]' %
                    (
                        self.datas[0].datetime.datetime(0).isoformat(),
                        self.data_close[0],
                        buy_compound, self.bbands.bold_1[0], self.p.buy_delta, self.atr[0]
                     )
                )
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            sell_compound = self.bbands.bolu_1[0] + (self.p.sell_delta * self.atr[0])
            if self.data_close[0] > sell_compound:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log(
                    'SELL CREATE %s (Close) %.2f > (Compound) %.2f :[BB_Low+(ATR * Sell delta) %.2f + %.2f * %.2f]' %
                    (
                        self.datas[0].datetime.datetime(0).isoformat(),
                        self.data_close[0],
                        sell_compound, self.bbands.bolu_1[0], self.p.sell_delta, self.atr[0]
                    )
                )
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))
                self.buy_price = order.executed.price
                self.buy_comm = order.executed.comm
            else: # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.map_period, self.broker.getvalue()), doprint=True)
