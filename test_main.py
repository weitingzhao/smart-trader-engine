from __future__ import (
    absolute_import, division, print_function,unicode_literals
)
import os
import logging
from cerebro.strategy_optimize import StrategyOptimize
from cerebro.strategy_profile import StrategyProfile
from strategy.strategy1stoperation import Strategy1stOperation

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)
# Configure logging
logging.basicConfig(filename='logs/backtrader_log.txt',
                    filemode='w',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


class JSONSaver:
    def __init__(self, json_data, file_path):
        self.json_data = json_data
        self.file_path = file_path

    def save_to_file(self):
        with open(self.file_path, 'w') as json_file:
            json_file.write(self.json_data)

def run_strategy(data_json, is_optimize=False):
    # Step 1. Convert the QuerySet to a DataFrame
    strategyProfile = StrategyOptimize(stdstats=False) if is_optimize else StrategyProfile(stdstats=True)
    # Step 2. Set Data
    strategyProfile.set_data(data_json = data_json)
    # Step 3. Set Strategy
    strategyProfile.set_strategy(Strategy1stOperation)
    # Step 4. Run the strategy
    strategyProfile.run()
    # Step 5. Save result to Json
    json_saver = JSONSaver(strategyProfile.result_json, 'results.json')
    json_saver.save_to_file()

    # Step 6. only Plot the strategy when is not optimize. optimize result is huge can't plot
    if not is_optimize or is_optimize:
        # strategyProfile.plot()
        strategyProfile.bokeh()
        return



if __name__ == '__main__':
    # Prepare the JSON object with parameters
    data_json = {
        'symbols': 'AVXL',
        'period': '6mo',  # Example period, replace with actual value if needed
        'interval': '60m',  # Example interval, replace with actual value if needed
        'since': '2024-07-01',
        # 'from': '2000-01-01',
        # 'to': '2000-12-31'
    }
    run_strategy(data_json, is_optimize=False)

