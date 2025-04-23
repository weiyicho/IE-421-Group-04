# strategies/strategy_1_volatility_breakout.py
import pandas as pd

def generate_volatility_compression_signals(df, bb_window: int = 20, percentile: float = 0.10, holding_period: int = 5):
    df = df.copy()
    df['MA'] = df['Close'].rolling(window=bb_window).mean()
    df['STD'] = df['Close'].rolling(window=bb_window).std()
    df['Upper'] = df['MA'] + 2 * df['STD']
    df['Lower'] = df['MA'] - 2 * df['STD']
    df['Band Width'] = (df['Upper'] - df['Lower']) / df['MA']

    bandwidth_threshold = df['Band Width'].rolling(window=252).quantile(percentile)
    signals = (df['Band Width'] < bandwidth_threshold).astype(int)

    bandwidth_40th = df['Band Width'].rolling(window=252).quantile(0.40)
    position = [0] * len(signals)
    holding = 0
    for i in range(len(signals)):
        if holding > 0:
            position[i] = 1
            holding -= 1
            if df['Band Width'].iloc[i] > bandwidth_40th.iloc[i]:
                holding = 0  # exit early if expansion starts
        elif signals.iloc[i] == 1:
            holding = holding_period
            position[i] = 1

    return pd.Series(position, index=df.index, name="Signal")