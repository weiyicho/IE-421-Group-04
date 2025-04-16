import openai
import pandas as pd


def summarize_data(price_data: pd.DataFrame) -> str:
    """
    Generate a textual summary of the intraday price data
    to be passed to the LLM.
    """
    description = price_data.describe().round(2).to_string()
    
    # Add example indicators
    price_data["returns"] = price_data["Close"].pct_change()
    volatility = price_data["returns"].std()
    rsi_sample = price_data["Close"].rolling(window=14).apply(
        lambda x: 100 - (100 / (1 + (x.diff().clip(lower=0).sum() / abs(x.diff().clip(upper=0)).sum()))), raw=False
    ).dropna()
    
    summary = f"""
        Intraday OHLCV data summary for SPY (5-minute bars over 5 days):
        - Volatility (std of returns): {volatility:.4f}
        - RSI (last 5 values): {rsi_sample.tail().round(2).to_dict()}
        - Basic stats:
        {description}
    """
    return summary

def gpt4_generate_strategy(data: pd.DataFrame, ticker: str = "SPY") -> str:
    """
    Uses GPT-4 to generate a trading strategy based on intraday data.

    Parameters:
    - price_data: DataFrame with OHLCV intraday data
    - ticker: the symbol (for context in the prompt)

    Returns:
    - Python code string for the strategy
    """
    # Get a simple summary of the data to give the model context
    preview = data.tail(30).to_csv(index=False)

    prompt = f"""
        You are a quantitative trader building an intraday trading strategy for the US stock {ticker}, using 5-minute OHLCV price data.

        Here is a recent snippet of the intraday price data (last 30 rows):

        {preview}

        Your task:
        - Create a trading strategy in Python using technical indicators such as RSI, VWAP, or EMA.
        - Use `pandas` and assume `price_data` is already available as a DataFrame with columns: ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
        - Generate clear buy/sell signals and store them in a new 'signal' column (1 = buy, -1 = sell, 0 = hold)
        - Keep the code simple, readable, and executable

        Respond ONLY with the code (no explanations).
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[ERROR] Strategy generation failed: {e}")
        return ""