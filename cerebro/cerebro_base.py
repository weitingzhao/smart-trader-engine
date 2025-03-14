import logging
import pandas as pd
import backtrader as bt
from cerebro.data.stock_hist_bars_yahoo import StockHistBarsYahoo
import contextlib
import io
from backtrader_plotting import Bokeh, OptBrowser
from backtrader_plotting.schemes import Tradimo
import os.path  # To manage paths
import datetime  # For datetime objects
import sys  # To find out the script name (in argv[0])
import json

class CustomPandasData(bt.feeds.PandasData):
    params = (
        ('plot', True),
        ('plotinfo', dict(plotstyle='candlestick')),
    )

class cerebroBase():

    def __init__(self, stdstats=False):
        # Create a cerebro entity
        self.cerebro = bt.Cerebro(stdstats=stdstats)
        self.data = None
        self.data_name = None
        self.data_df = None
        self.strategy  = None

        # Result
        self.result = None
        self.result_df = None
        self.result_json = None


    def set_data(self, data_json : object):

        # Extract symbols from JSON
        symbols = data_json.get('symbols')
        # Continue with the rest of your logic
        period = data_json.get('period')
        interval = data_json.get('interval')
        since = data_json.get('since')
        from_ = data_json.get('from')
        to_ = data_json.get('to')

        # Build the meta dictionary based on input
        meta = {
            'error': 'false',
            'output': '',
            'status': 'STARTED',
            'initial': 'false',
            'leftover': symbols.split('|'),
            'done': []
        }

        # Prepare args dictionary
        args = f"snapshot=True,period='{period}',interval='{interval}',symbols={symbols},since={since}"

        # Call the function to get Yahoo data
        worker = StockHistBarsYahoo()
        error_list, meta = worker.run(meta=meta, args=args, is_test=False)
        if len(error_list) > 0:
            return
        yahoo_data = worker.snapshot
        # Convert yahoo_data to a DataFrame
        yahoo_data_df = pd.DataFrame(yahoo_data)

        # # Step 1.  Prepare data as Data Frame
        # Filter the DataFrame by the 'since' date
        if from_:
            stock_data_df = yahoo_data_df[(yahoo_data_df.index >= from_) & (yahoo_data_df.index <= to_)]
        else:
            stock_data_df = yahoo_data_df[yahoo_data_df.index >= since]

        stock_data_df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume',
        }, inplace=True)
        # Remove the 'dividends' and 'stocksplits' columns
        stock_data_df.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
        stock_data_df.rename_axis('datetime', inplace=True)
        # Add the openinterest column and set it to 0
        stock_data_df['openinterest'] = 0

        # Set Data Name
        self.data_name = f'{symbols}-{since}'
        self.data_df = stock_data_df

    def _prepare_data(self):
        # Add the Data Feed to Cerebro
        self.data = bt.feeds.PandasData(dataname=self.data_df)
        self.data._name = self.data_name
        self.cerebro.adddata(self.data)

    def set_strategy(self, strategy):
        self.strategy = strategy

    def configure(self):

        # Part 1. Broker
        #           Set our desired cash start
        self.cerebro.broker.setcash(1000.0)
        #           Add a FixedSize sizer according to the stake
        self.cerebro.addsizer(bt.sizers.FixedSize, stake=10)
        #           Set the Commission - 0.1% ... divide by 100 to remove the %
        self.cerebro.broker.setcommission(commission=0.001)

        # Part 2. Analyzers
        self.cerebro.addanalyzer(bt.analyzers.SQN)
        self.cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)
        self.cerebro.addanalyzer(bt.analyzers.DrawDown)
        self.cerebro.addanalyzer(bt.analyzers.Returns)
        # self.cerebro.addanalyzer(bt.analyzers.PyFolio) # will throw error if add this one

        # Part 3. Observer
        self.cerebro.addobserver(bt.observers.DrawDown)  # visualize the drawdown evol
        self.cerebro.addobserver(bt.observers.Broker)


    def print_result(self):
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

    def plot(self):
        self.print_result()

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
        # Save the plot as an image
        # Plot the result
        bokeh = Bokeh(
            # kwargs
            style='bar', plot_mode='single',
            # params
            scheme=Tradimo(), output_mode='memory')

        self.cerebro.plot(bokeh, iplot=False)
        browser = OptBrowser(bokeh, self.result)
        browser.start()

    def get_data_csv_example(self):
        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, 'datas/orcl-1995-2014.txt')
        # # Create a Data Feed
        # data = bt.feeds.YahooFinanceCSVData(
        #     dataname=datapath,
        #     # Do not pass values before this date
        #     fromdate=datetime.datetime(2000, 1, 1),
        #     # Do not pass values after this date
        #     todate=datetime.datetime(2000, 12, 31),
        #     reverse=False)
        pass

    def flatten_dict(self, d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f'{parent_key}{sep}{k}' if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

