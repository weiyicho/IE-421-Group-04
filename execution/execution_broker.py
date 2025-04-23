# execution_broker.py

from ib_insync import *
import time
import asyncio

class ExecutionBroker:
    def __init__(self, mode='paper', capital=100_000, host='127.0.0.1', port=7497, client_id=123):
        self.mode = mode
        self.cash = capital
        self.positions = {}  # {ticker: size}

        if mode in ['paper', 'live']:
            self.ib = IB()
            if asyncio.get_event_loop().is_running():
                # Jupyter-safe async connection
                future = asyncio.ensure_future(self.ib.connectAsync(host, port, clientId=client_id))
                while not self.ib.isConnected():
                    time.sleep(0.1)
            else:
                self.ib.connect(host, port, clientId=client_id)
            print(f"✅ Connected to IBKR ({mode.upper()})")

    def submit_order(self, ticker: str, signal: int, price=None, size=None):
        if signal == 0:
            return

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

        action = 'BUY' if signal == 1 else 'SELL'
        size = size or 1
        order = MarketOrder(action, size)
        trade = self.ib.placeOrder(contract, order)

        print(f"[IBKR] {action} {size} {ticker} submitted...")

    # Async-friendly logic (Jupyter safe)
        if asyncio.get_event_loop().is_running():
            def on_fill(trade, fill):
                print(f"[IBKR] ✅ Filled: {fill.execution}")
            trade.filledEvent += on_fill
        else:
            while not trade.isDone():
                self.ib.waitOnUpdate()
            print(f"[IBKR] ✅ Order status: {trade.orderStatus.status}")

        def disconnect(self):
            if self.mode in ['paper', 'live']:
                self.ib.disconnect()
                print("❎ Disconnected from IBKR.")
