from agent.data_fetch import fetch_intraday_data
from agent.strategy import generate_strategy
#from agent.eval import backtest

import pandas as pd
import numpy as np


data = fetch_intraday_data("TSLA", "5m", "5d", True)

code, strat = generate_strategy(data, "Come up with a profitable strategy on TSLA")

print(data.head())
print(code)