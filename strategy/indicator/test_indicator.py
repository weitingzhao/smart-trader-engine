import backtrader as bt
import numpy as np


class DummyIndicator(bt.Indicator):
    # 将计算的指标命名为 'dummyline'，后面调用这根 line 的方式有：
    # self.lines.dummyline ↔ self.l.dummyline ↔ self.dummyline
    lines = ('dummyline',)
    # 定义参数，后面调用这个参数的方式有：
    # self.params.xxx ↔ self.p.xxx
    params = (('value', 5),)

    def __init__(self):
        self.l.dummyline = bt.Max(0.0, self.p.value)

    def next(self):
        self.l.dummyline[0] = max(0.0, self.p.value)

    def once(self, start, end):
        dummy_array = self.l.dummyline.array
        for i in range(start, end):
            dummy_array[i] = max(0.0, self.p.value)
