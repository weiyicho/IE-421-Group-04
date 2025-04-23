# strategies/strategy_3_sentiment_swing.py
import pandas as pd

def add_rsi(df, period=14):
    delta = df['SPY'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss

    df['RSI'] = 100 - (100 / (1 + rs))
    return df

def generate_rsi_divergence_signals(df, lookback=10, holding=5):
    df = df.copy()
    df = add_rsi(df)

    signals = [0] * len(df)
    position = [0] * len(df)
    hold = 0

    for i in range(lookback, len(df)):
        price_now = df['SPY'].iloc[i]
        price_then = df['SPY'].iloc[i - lookback]
        rsi_now = df['RSI'].iloc[i]
        rsi_then = df['RSI'].iloc[i - lookback]

        # Bullish divergence: price down, RSI up
        if price_now < price_then and rsi_now > rsi_then and rsi_now < 50 and not hold:
            hold = holding
            signals[i] = 1

        if hold > 0:
            position[i] = 1
            hold -= 1

    return pd.Series(position, index=df.index, name="Signal")

def generate_rsi_divergence_with_trend_filter(df, lookback=10, holding=5):
    df = df.copy()
    df = add_rsi(df)
    df['MA200'] = df['SPY'].rolling(window=200).mean()

    signals = [0] * len(df)
    position = [0] * len(df)
    hold = 0
    direction = 0  # 1 = long, -1 = short

    for i in range(lookback, len(df)):
        price_now = df['SPY'].iloc[i]
        price_then = df['SPY'].iloc[i - lookback]
        rsi_now = df['RSI'].iloc[i]
        rsi_then = df['RSI'].iloc[i - lookback]
        ma200 = df['MA200'].iloc[i]

        # Start new trade if not currently holding
        if hold == 0:
            # Bullish divergence: price down, RSI up, RSI < 50
            if price_now < price_then and rsi_now > rsi_then and rsi_now < 50:
                hold = holding
                direction = 1
                signals[i] = 1

            # Bearish divergence: price up, RSI down, RSI > 50 + SPY below MA200
            elif (
                price_now > price_then
                and rsi_now < rsi_then
                and rsi_now > 50
                and price_now < ma200  # ← trend filter for shorting
            ):
                hold = holding
                direction = -1
                signals[i] = -1

        else:
            signals[i] = direction
            hold -= 1

    return pd.Series(signals, index=df.index, name="Signal")
