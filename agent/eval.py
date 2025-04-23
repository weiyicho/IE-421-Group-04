import pandas as pd
import numpy as np

def backtest_strategy(df, strategy_code: str):
    return " "

def generate_report(results: dict, strategy_description: str):
    print("\n--- STRATEGY REPORT ---")
    print("Description:", strategy_description)
    print("Cumulative Return:", round(results["cumulative_return"], 4))
    print("Sharpe Ratio:", round(results["sharpe"], 4))
    print("------------------------")