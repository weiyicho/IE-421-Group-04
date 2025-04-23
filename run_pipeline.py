from execution_broker import ExecutionBroker

broker = ExecutionBroker(mode='paper')

# In your signal loop:
for date, row in df.iterrows():
    signal = row['Signal']
    price = row['Close']

    if signal != 0:
        broker.submit_order(ticker='SPY', signal=signal, price=price)

broker.disconnect()