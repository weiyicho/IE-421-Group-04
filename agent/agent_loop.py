from data_fetch import fetch_intraday_data
from agent.strategy import generate_strategy
from agent.eval import backtest_strategy, generate_report


def run_agent(
    prompt: str = "Come up with a profitable strategy on SPY",
    ticker: str = "SPY",
    interval: str = "5m",
    period: str = "5d",
    use_cache: bool = True
):
    print(f"\n[🔍] Step 1: Fetching Data for {ticker}...")
    data = fetch_intraday_data(ticker, interval, period, use_cache)
    if data.empty:
        print("[❌] No data available. Exiting agent.")
        return

    print(f"\n[🧠] Step 2: Generating Strategy...")
    strategy_code, strategy_description = generate_strategy(data, prompt)

    print(f"\n[📈] Step 3: Backtesting Strategy...")
    results = backtest_strategy(data, strategy_code)

    print(f"\n[📝] Step 4: Generating Report...")
    generate_report(results, strategy_description)

    print("\n✅ Agent run complete.")