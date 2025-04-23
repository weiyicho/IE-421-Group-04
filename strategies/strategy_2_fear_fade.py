# strategies/strategy_2_fear_fade.py
import pandas as pd

def generate_vix_fade_v2_with_stop(df, vix_window=252, high_percentile=0.90, low_percentile=0.60, stop_loss=-0.035, max_hold=5):
    df = df.copy()
    df['VIX_high'] = df['VIX'].rolling(window=vix_window).quantile(high_percentile)
    df['VIX_low'] = df['VIX'].rolling(window=vix_window).quantile(low_percentile)
    df['SPY_ret'] = df['SPY'].pct_change().fillna(0)

    position = [0] * len(df)
    in_trade = False
    hold_days = 0
    entry_price = 0.0

    for i in range(1, len(df)):
        if not in_trade:
            if df['VIX'].iloc[i] > df['VIX_high'].iloc[i] and df['SPY_ret'].iloc[i] < 0:
                in_trade = True
                hold_days = 1
                entry_price = df['SPY'].iloc[i]
                position[i] = 1
        else:
            hold_days += 1
            current_price = df['SPY'].iloc[i]
            pnl = (current_price - entry_price) / entry_price
            position[i] = 1

            # Exit conditions: VIX calmed, max hold, or SPY dropped too much
            if (
                df['VIX'].iloc[i] < df['VIX_low'].iloc[i]
                or hold_days >= max_hold
                or pnl <= stop_loss
            ):
                in_trade = False
                hold_days = 0

    return pd.Series(position, index=df.index, name="Signal")
