import backtrader as bt
from strategy.indicator.test_bollinger_bands import CustomBollingerBands
import matplotlib.pyplot as plt
import backtrader.indicators as btind

# Create a Stratey
class Strategy1stOperation(bt.Strategy):
    params = (
        ('map_period', 10),
        ('printlog', False),
    )


    def log(self, txt, dt=None, doprint=False):
        ''' Logging function for this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))



    def __init__(self):
        self.plot_objects = None  # Initialize plot_objects to store plot references

        # Keep a reference to the "close" line in the data[0] dataseries
        self.data_close = self.datas[0].close

        # To keep track of pending orders
        self.order = None
        self.buy_price = None
        self.buy_comm = None
        self.bar_executed = 0

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.map_period)

        # Let's put rsi on stochastic/sma or the other way round
        # self.stoc = btind.Stochastic()

        # Indicators for the plotting show
        # Nadaraya smoothed flux charts with three different bands
        self.custom_bbands = CustomBollingerBands(self.data)

        # self.nadaraya_bb = NadarayaBollingerBands()
        # self.dummy_idx = DummyIndicator()

        # Add Bollinger Bands indicator
        # bt.indicators.BollingerBands(self.datas[0], period=20, devfactor=3)
        bt.indicators.MACDHisto(self.datas[0])

        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.RSI(self.datas[0])
        # bt.indicators.ATR(self.datas[0], plot=False)

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


    def next(self):
        # Get the max and min from Bollinger Bands
        bb = self.custom_bbands

        # Dynamically adjust plot range
        # if self.plot_objects:
        #     self.update_yaxis_range(bolu_max, bolu_min)

        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.data_close[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.data_close[0] > self.sma[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.data_close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
        else:
            if self.data_close[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.data_close[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()


    def update_yaxis_range(self, bolu_max, bolu_min):
        """Custom method to adjust Y-axis range."""
        for figure in self.plot_objects[0].figures.values():
            for axis in figure.axises:
                if hasattr(axis, 'set_ylim'):
                    axis.set_ylim(bolu_min * 0.95, bolu_max * 1.05)  # Add buffer for aesthetics

    # Custom Plotting Logic
    def custom_plot(cerebro):
        fig, axes = cerebro.plot()[0]  # Get the figure and axes

        # Adjust Y-axis dynamically for the main plot
        for ax in axes:
            if ax.get_title() == 'Data0':  # The main plot with data
                # Find Bollinger Bands max and min
                bb_lines = ax.lines[-3:]  # Last 3 lines: bolu_1, bolu_2, mid
                bolu_1, bolu_2 = bb_lines[0].get_ydata(), bb_lines[1].get_ydata()

                # Calculate the overall range
                y_max = max(max(bolu_1), max(bolu_2))
                y_min = min(min(bolu_1), min(bolu_2))

                # Adjust the Y-axis range
                ax.set_ylim(y_min * 0.95, y_max * 1.05)

        # Show the plot
        plt.show()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.map_period, self.broker.getvalue()), doprint=True)
