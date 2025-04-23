# execution_broker.py

from ib_insync import *
import time

class ExecutionBroker:
    def __init__(self, mode='paper', capital=100_000, host='127.0.0.1', port=7497, client_id=1):
        self.mode = mode
        self.cash = capital
        self.positions = {}  # {ticker: size}

        if mode in ['paper', 'live']:
            self.ib = IB()
            self.ib.connect(host, port, clientId=client_id)
            print(f"Connected to IBKR ({mode})")

    def submit_order(self, ticker: str, signal: int, price=None, size=None):
        if self.mode == 'backtest':
            self._simulate_order(ticker, signal, price, size)
        else:
            self._submit_ib_order(ticker, signal, size)

    def _simulate_order(self, ticker, signal, price, size):
        size = size or int(self.cash * 0.01 / price)
        if signal == 1:
            self.positions[ticker] = self.positions.get(ticker, 0) + size
            self.cash -= size * price
        elif signal == -1:
            size = min(size or self.positions.get(ticker, 0), self.positions.get(ticker, 0))
            self.positions[ticker] -= size
            self.cash += size * price

        print(f"[SIM] {'BUY' if signal == 1 else 'SELL'} {size} {ticker} @ {price:.2f}")

    def _submit_ib_order(self, ticker, signal, size):
        contract = Stock(ticker, 'SMART', 'USD')
        self.ib.qualifyContracts(contract)

        order_type = 'MKT'
        action = 'BUY' if signal == 1 else 'SELL'
        size = size or 10

        order = MarketOrder(action, size)
        trade = self.ib.placeOrder(contract, order)
        print(f"[IBKR] {action} {size} {ticker} submitted...")

        self.ib.sleep(1)
        while not trade.isDone():
            self.ib.waitOnUpdate()
        print(f"[IBKR] Order filled: {trade.orderStatus}")

    def disconnect(self):
        if self.mode in ['paper', 'live']:
            self.ib.disconnect()
            print("Disconnected from IBKR.")
