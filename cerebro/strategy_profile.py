import json
import pandas as pd

from cerebro.cerebro_base import cerebroBase

# @ray.remote
class StrategyProfile(cerebroBase):

    def __init__(self, stdstats=False):
        super().__init__(stdstats)


    def run(self):
        # Prepare data
        self._prepare_data()
        # Configure
        self.configure()
        # Add Strategy
        self.cerebro.addstrategy(
            self.strategy,
            buy_delta=0.50,
            sell_delta=0.50,
        )
        # Run cerebro
        self.result = self.cerebro.run(optreturn=True)
        self.results_to_dataframe()
        return self.result


    def results_to_dataframe(self):
        json_results = []
        df_results = []

        for strat in self.result:
            for analyz in strat.analyzers:
                result = analyz.get_analysis()

                json_results.append(result)
                df_results.append(self.flatten_dict(result))

        self.result_json = json.dumps(json_results, indent=4)
        self.result_df = pd.DataFrame(df_results)