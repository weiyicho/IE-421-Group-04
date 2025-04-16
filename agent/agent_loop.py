from data_fetch import fetch_intraday_data
from strategy import gpt4_generate_strategy, gpt4_improve_strategy


while not success:
    data = fetch_intraday_data('SPY')
    strategy_code = gpt4_generate_strategy(data)
    # backtest strat
    """
    if **some performance metric***:
        success = True
    else:
        strategy_code = gpt4_improve_strategy(performance)
    """