import backtrader as bt
import numpy as np

class BollingerBifrostStrategy(bt.Strategy):
    params = dict(
        h=6,  # Smoothing factor for Nadaraya-Watson estimator
        repaint=False,
        short_period=20,
        short_stdev=3,
        med_period=75,
        med_stdev=4,
        long_period=100,
        long_stdev=4.25,
        notify_cross=True,
    )

    def __init__(self):
        # Define typical price
        self.tp = (self.data.high + self.data.low + self.data.close) / 3

        # Bollinger Bands for different periods
        self.bollinger_short = self.calc_bollinger(self.params.short_period, self.params.short_stdev)
        self.bollinger_med = self.calc_bollinger(self.params.med_period, self.params.med_stdev)
        self.bollinger_long = self.calc_bollinger(self.params.long_period, self.params.long_stdev)

        # Smoothing using Nadaraya-Watson estimator
        self.smooth_boll_short_upper = self.nadaraya_watson(self.bollinger_short['upper'])
        self.smooth_boll_short_lower = self.nadaraya_watson(self.bollinger_short['lower'])

        # Alerts
        self.crossed_upper = False
        self.crossed_lower = False

    def calc_bollinger(self, period, stdev):
        sma = bt.indicators.SimpleMovingAverage(self.tp, period)
        std = bt.indicators.StandardDeviation(self.tp, period)
        upper = sma + (stdev * std)
        lower = sma - (stdev * std)
        return {'sma': sma, 'upper': upper, 'lower': lower}

    def nadaraya_watson(self, src):
        """Smooth the series using a Nadaraya-Watson estimator."""
        h = self.params.h
        n = len(src.array)

        weights = np.exp(-0.5 * (np.arange(-n + 1, 1) ** 2) / (h ** 2))
        weights /= np.sum(weights)

        smoothed = np.convolve(src.array, weights, mode='valid')
        return bt.LineSeries(data=smoothed)

    def next(self):
        # Check for crosses
        close = self.data.close[0]
        smooth_upper = self.smooth_boll_short_upper[0]
        smooth_lower = self.smooth_boll_short_lower[0]

        if close > smooth_upper:
            if not self.crossed_upper and self.params.notify_cross:
                self.log(f"Upper Band Crossed: {close}")
                self.crossed_upper = True
            self.crossed_lower = False  # Reset the lower cross flag

        elif close < smooth_lower:
            if not self.crossed_lower and self.params.notify_cross:
                self.log(f"Lower Band Crossed: {close}")
                self.crossed_lower = True
            self.crossed_upper = False  # Reset the upper cross flag

    def log(self, text):
        dt = self.datas[0].datetime.datetime(0)
        print(f"{dt}: {text}")