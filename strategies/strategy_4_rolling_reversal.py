# strategies/strategy_4_rolling_reversal.py

import pandas as pd

def add_trend_and_volatility(df, ma_period=50, atr_period=14):
    df = df.copy()
    df['MA'] = df['SPY'].rolling(window=ma_period).mean()

    high_low = df['SPY'].rolling(2).max() - df['SPY'].rolling(2).min()
    high_close = abs(df['SPY'] - df['SPY'].shift(1))
    tr = pd.concat([high_low, high_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(atr_period).mean()

    return df

def generate_rolling_reversal_v3(df, ma_period=50, atr_period=14, atr_window=50,
                                 atr_thresh=0.7, holding=5, stop_loss=0.03):
    df = add_trend_and_volatility(df, ma_period, atr_period)

    df['ATR_Perc'] = df['ATR'].rolling(atr_window).apply(
        lambda x: (x.iloc[-1] - x.min()) / (x.max() - x.min()) if (x.max() - x.min()) > 0 else 1.0,
        raw=False
    )

    signals = [0] * len(df)
    hold = 0
    direction = 0
    entry_price = 0

    for i in range(ma_period, len(df)):
        price = df['SPY'].iloc[i]
        ma = df['MA'].iloc[i]
        atr_perc = df['ATR_Perc'].iloc[i]

        # If in trade, check stop-loss or continue
        if hold > 0:
            change = (price - entry_price) / entry_price * direction
            if change <= -stop_loss:
                hold = 0
                direction = 0
            else:
                signals[i] = direction
                hold -= 1
            continue

        # Only enter a new trade if not holding
        if atr_perc <= atr_thresh:
            if price > ma * 0.985 and price < ma:  # Small pullback
                hold = holding
                direction = 1
                entry_price = price
                signals[i] = 1
            elif price < ma and price > ma * 1.015:  # short entry
                hold = holding
                direction = -1
                entry_price = price
                signals[i] = -1

    return pd.Series(signals, index=df.index, name="Signal")
