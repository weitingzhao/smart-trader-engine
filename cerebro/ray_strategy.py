import contextlib
import io
import ray

from backtrader_plotting import Bokeh, OptBrowser
from backtrader_plotting.schemes import Tradimo
from cerebro.cerebro_base import cerebroBase
from .strategy.test_strategy_1st import TestStrategy

# @ray.remote
class RayStrategyProfile(cerebroBase):

    def __init__(self, stdstats=False):
        super().__init__(stdstats)


    def run(self):
        # Prepare data
        self._prepare_data()
        # Configure
        self.configure()
        # Add Strategy
        self.cerebro.addstrategy(self.strategy, map_period=13)
        # Run cerebro
        self.result = self.cerebro.run(optreturn=True)
        return self.result

    def plot(self):
        colors = [
            '#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a8786e',
            '#ed97ca', '#a2a2a2', '#cdcc5d', '#6dccda']

        # Last Step Plot : Default
        self.cerebro.plot(
            iplot=False,  # 在 Jupyter Notebook 上绘图时是否自动 plot inline
            style='candel',  # 设置主图行情数据的样式为蜡烛图
            lcolors=colors,  # 重新设置主题颜色
            plotdist=0.1,  # 设置图形之间的间距
            bartrans=0.2,  # 设置蜡烛图的透明度
            barup='#98df8a', bardown='#ff9896',  # 设置蜡烛图上涨和下跌的颜色
            volup='#98df8a', voldown='#ff9896',  # 设置成交量在行情上涨和下跌情况下的颜色
            loc='#5f5a41',
            plotter=None,  # 包含各种绘图属性的对象或类，如果为None，默认取 PlotScheme 类，如下所示
            numfigs=1,  # 是否将图形拆分成多幅图展示，如果时间区间比较长，建议分多幅展示
        )  # 对应 PlotScheme 中的各个参数

    def bokeh(self):
        st0 = self.result[0]
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            for alyzer in st0.analyzers:
                alyzer.print()
        analysis_result = output.getvalue()
        output.close()

        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        # Save the plot as an image
        # Plot the result
        bokeh = Bokeh(
            # kwargs
            style='bar', plot_mode='single',
            # params
            scheme=Tradimo(), output_mode='memory')

        self.cerebro.plot(bokeh, iplot=False)
        # plot = bokeh.plot_html(bokeh.figurepages[0].model, template="smart_trader.html.j2")

        browser = OptBrowser(bokeh, self.result)
        browser.start()
