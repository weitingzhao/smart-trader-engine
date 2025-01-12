from __future__ import (
    absolute_import, division, print_function,unicode_literals
)

from bokeh.model import Model
from backtrader_plotting.bokeh import BokehWebapp
from cerebro.ray_strategy import RayStrategyProfile
from strategy.strategy1stoperation import Strategy1stOperation


def plot_bokeh(result, strategyProfile : RayStrategyProfile):
    analysis_result, bokeh  = strategyProfile.plot()
    # # B. For Add Strategy
    def build_optresult_model(self, _=None) -> Model:
        return bokeh.figurepages[0].model

    webapp = BokehWebapp(
        title="Backtrader Optimization Result",
        html_template="basic.html.j2",
        scheme=bokeh.params.scheme,
        model_factory_fnc=build_optresult_model)
    webapp.start()

def plot_default(result, strategyProfile : RayStrategyProfile):

    colors = [
        '#729ece', '#ff9e4a', '#67bf5c', '#ed665d', '#ad8bc9', '#a8786e',
        '#ed97ca', '#a2a2a2', '#cdcc5d','#6dccda']

    # Last Step Plot : Default
    strategyProfile.cerebro.plot(
        iplot=False, # 在 Jupyter Notebook 上绘图时是否自动 plot inline
        style='candel',  # 设置主图行情数据的样式为蜡烛图
        lcolors=colors,  # 重新设置主题颜色
        plotdist=0.1,  # 设置图形之间的间距
        bartrans=0.2, # 设置蜡烛图的透明度
        barup='#ff9896', bardown='#98df8a',  # 设置蜡烛图上涨和下跌的颜色
        volup='#ff9896', voldown='#98df8a',  # 设置成交量在行情上涨和下跌情况下的颜色
        loc='#5f5a41',
        plotter=None, # 包含各种绘图属性的对象或类，如果为None，默认取 PlotScheme 类，如下所示
        numfigs=1, # 是否将图形拆分成多幅图展示，如果时间区间比较长，建议分多幅展示
        ) # 对应 PlotScheme 中的各个参数


# def plot_return_analysis(result, strategyProfile : RayStrategyProfile):
#     # 提取收益序列
#     pnl = pd.Series(result[0].analyzers._TimeReturn.get_analysis())
#     # 计算累计收益
#     cumulative = (pnl + 1).cumprod()
#     # 计算回撤序列
#     max_return = cumulative.cummax()
#     drawdown = (cumulative - max_return) / max_return
#     # 计算收益评价指标
#     import pyfolio as pf
#     # 按年统计收益指标
#     perf_stats_year = (pnl).groupby(pnl.index.to_period('y')).apply(
#         lambda data: pf.timeseries.perf_stats(data)).unstack()
#     # 统计所有时间段的收益指标
#     perf_stats_all = pf.timeseries.perf_stats((pnl)).to_frame(name='all')
#     perf_stats = pd.concat([perf_stats_year, perf_stats_all.T], axis=0)
#     perf_stats_ = round(perf_stats, 4).reset_index()
#
#     # 绘制图形
#     import matplotlib.pyplot as plt
#     plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#     import matplotlib.ticker as ticker  # 导入设置坐标轴的模块
#     plt.style.use('seaborn')  # plt.style.use('dark_background')
#
#     fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1.5, 4]}, figsize=(20, 8))
#     cols_names = ['date', 'Annual\nreturn', 'Cumulative\nreturns', 'Annual\nvolatility',
#                   'Sharpe\nratio', 'Calmar\nratio', 'Stability', 'Max\ndrawdown',
#                   'Omega\nratio', 'Sortino\nratio', 'Skew', 'Kurtosis', 'Tail\nratio',
#                   'Daily value\nat risk']
#
#     # 绘制表格
#     ax0.set_axis_off()  # 除去坐标轴
#     table = ax0.table(cellText=perf_stats_.values,
#                       bbox=(0, 0, 1, 1),  # 设置表格位置， (x0, y0, width, height)
#                       rowLoc='right',  # 行标题居中
#                       cellLoc='right',
#                       colLabels=cols_names,  # 设置列标题
#                       colLoc='right',  # 列标题居中
#                       edges='open'  # 不显示表格边框
#                       )
#     table.set_fontsize(13)
#
#     # 绘制累计收益曲线
#     ax2 = ax1.twinx()
#     ax1.yaxis.set_ticks_position('right')  # 将回撤曲线的 y 轴移至右侧
#     ax2.yaxis.set_ticks_position('left')  # 将累计收益曲线的 y 轴移至左侧
#     # 绘制回撤曲线
#     drawdown.plot.area(ax=ax1, label='drawdown (right)', rot=0, alpha=0.3, fontsize=13, grid=False)
#     # 绘制累计收益曲线
#     (cumulative).plot(ax=ax2, color='#F1C40F', lw=3.0, label='cumret (left)', rot=0, fontsize=13, grid=False)
#     # 不然 x 轴留有空白
#     ax2.set_xbound(lower=cumulative.index.min(), upper=cumulative.index.max())
#     # 主轴定位器：每 5 个月显示一个日期：根据具体天数来做排版
#     ax2.xaxis.set_major_locator(ticker.MultipleLocator(100))
#     # 同时绘制双轴的图例
#     h1, l1 = ax1.get_legend_handles_labels()
#     h2, l2 = ax2.get_legend_handles_labels()
#     plt.legend(h1 + h2, l1 + l2, fontsize=12, loc='upper left', ncol=1)
#
#     fig.tight_layout()  # 规整排版
#     plt.show()

def ideal_main():
    # Prepare the JSON object with parameters
    data_json = {
        'symbols': 'DAVE',
        'period': '3mo',  # Example period, replace with actual value if needed
        'interval': '60m',  # Example interval, replace with actual value if needed
        'since': '2024-05-01',
        # 'from': '2000-01-01',
        # 'to': '2000-12-31'
    }

    # Step 1. Convert the QuerySet to a DataFrame
    strategyProfile = RayStrategyProfile(stdstats=True)
    # Step 2. Set Data
    strategyProfile.set_data(data_json = data_json)
    # Step 3. Load Startegy
    strategyProfile.set_strategy(Strategy1stOperation)
    # Step 4. Run the strategy
    result = strategyProfile.run()

    # Step 5. Plot the strategy
    plot_default(result, strategyProfile)
    # plot_return_analysis(result, strategyProfile)

if __name__ == '__main__':
    ideal_main()