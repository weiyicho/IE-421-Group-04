from agent.data_fetch import fetch_intraday_data
from agent.strategy import gpt4_generate_strategy, summarize_data
from agent.eval import backtest

import pandas as pd
import numpy as np


def strat(price_data: pd.DataFrame, ticker: str = "SPY") -> pd.DataFrame:
    # Calculate RSI
    price_data['RSI'] = price_data['Close'].rolling(14).apply(
        lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0)).sum()))),
        raw=False
    )

    # Force VWAP to align properly as Series
    vwap = (price_data['Close'] * price_data['Volume']).cumsum() / price_data['Volume'].cumsum()
    price_data['VWAP'] = pd.Series(vwap, index=price_data.index)

    # Drop rows with NaNs (caused by rolling RSI)
    price_data.dropna(inplace=True)

    # Strategy Logic
    price_data['signal'] = 0
    price_data.loc[(price_data['RSI'] < 40) & (price_data['Close'] < price_data['VWAP']), 'signal'] = 1
    price_data.loc[(price_data['RSI'] > 60) & (price_data['Close'] > price_data['VWAP']), 'signal'] = -1

    return price_data



df = fetch_intraday_data("SPY", interval="5m", period="5d")
fin = strat(df, ticker="SPY")

print(backtest(fin))    