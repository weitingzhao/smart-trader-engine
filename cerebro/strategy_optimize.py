import ray
from cerebro.cerebro_base import cerebroBase
from pandas.core.interchange.dataframe_protocol import DataFrame
import numpy as np
import json
import pandas as pd
import datetime
from datetime import datetime
from collections import OrderedDict

# Function to convert datetime keys to strings recursively
def convert_datetime_keys(obj):
    if isinstance(obj, list):
        return [convert_datetime_keys(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(k) if isinstance(k, datetime) else k: convert_datetime_keys(v) for k, v in obj.items()}
    elif isinstance(obj, OrderedDict):
        return OrderedDict((str(k) if isinstance(k, datetime) else k, convert_datetime_keys(v)) for k, v in obj.items())
    else:
        return obj


# @ray.remote
class StrategyOptimize(cerebroBase):

    def __init__(self, stdstats=False):
        super().__init__(stdstats)


    def run(self) -> DataFrame:
        # Prepare data
        self._prepare_data()
        # Configure
        self.configure()
        # Add Strategy
        self.cerebro.optstrategy(
            self.strategy,
            buy_delta=np.arange(1, 0, -0.5),
            sell_delta=np.arange(1, 0, -0.5),
        )

        # Run cerebro
        self.result = self.cerebro.run(optreturn=True)
        self.results_to_dataframe()
        return self.result

    # Custom serializer


    def results_to_dataframe(self):
        json_results = []

        for strat in self.result:
            analyzes = [analyze.get_analysis() for analyze in strat[0].analyzers]
            json_results.append({"params": strat[0].params.__dict__, "analyze":analyzes})

        # Preprocess data to convert datetime keys to strings
        # processed_data = convert_datetime_keys(json_results)

        self.result_json = json.dumps(json_results, indent=4)