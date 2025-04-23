from execution.execution_broker import ExecutionBroker
from strategies.strategy_1_volatility_breakout import generate_volatility_compression_signals
from datasets.data_fetch import fetch_data

broker = ExecutionBroker(mode='paper')

df = fetch_data("SPY", start="2025-04-21")
df['Signal'] = generate_volatility_compression_signals(df)
print(df[['Close', 'Signal']].tail())
# In your signal loop:
for date, row in df.iterrows():
    signal = row['Signal'].item()  # extract scalar value
    price = row['Close'].item()

    if signal != 0:
        print(f"Submitting order: {signal} at {price} on Date: {date}")
        #broker.submit_order(ticker='SPY', signal=signal, price=price)

# broker.disconnect()