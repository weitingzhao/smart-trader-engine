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



def ideal_main():
    # Prepare the JSON object with parameters
    data_json = {
        'symbols': 'HIMS',
        'period': '3mo',  # Example period, replace with actual value if needed
        'interval': '60m',  # Example interval, replace with actual value if needed
        'since': '2024-07-01',
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
    strategyProfile.run()
    # Step 5. Plot the strategy
    # strategyProfile.plot()
    strategyProfile.bokeh()


if __name__ == '__main__':
    ideal_main()