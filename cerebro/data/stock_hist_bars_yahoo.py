import logging, re
import yfinance as yf
from typing import List
from .base_service import BaseService
from .task_fetching_worker import TaskFetchingWorker

class StockHistBarsYahoo(BaseService, TaskFetchingWorker):

    def __init__(self):
        super().__init__()
        self.symbol_data = None
        self.snapshot = None

    @staticmethod
    def _use_day_table(interval: str) -> bool:
        return interval == "1d" or interval == "1wk" or interval == "1mo" or interval == "3mo"

    #Simluate for test use only
    def _get_init_load_test(self)->List:
        return ["TTEK"]

    def _get_init_load(self) -> List:
        return []

    def _before_fetching(self, records: List) -> any:
        return yf.Tickers(" ".join(records))

    def _fetching_detail(self, record: str, tools: any):
        # Simulate real workload
        # time.sleep(1)

        # Step 1. prepare parameters
        #method for append
        is_snapshot = self.args.get("snapshot", False)
        is_append = self.args.get("append",False)
        delta= int(self.args.get("delta", 1))
        # “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
        interval = self.args.get("interval", "max") #"1d"
        # “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
        if self.symbol_data is None:
            period = self.args.get("period", "1m")
        else:
            period = self.symbol_data[record]["period"]

        #If not using period – in the format (yyyy-mm-dd) or datetime.
        start = self.args.get("start", None)
        end = self.args.get("end", None)
        # the stocker tools
        ticker = tools.tickers[record]

        # Step 3. Saving.
        try:
            if start:
                history = ticker.history(start=start, end=end, interval=interval)
                if is_snapshot:
                    self.snapshot = history
                    return
            else:
                history = ticker.history(period=period, interval=interval)
                if is_snapshot:
                    self.snapshot = history
                    return
        except Exception as e:
            print(f"Error fetching data got error: {e}")
            # Optionally, you could return a custom value or re-raise the exception
            return None
