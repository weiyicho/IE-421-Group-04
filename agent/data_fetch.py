import yfinance as yf
import pandas as pd

def fetch_intraday_data(name: str="SPY", interval: str='5m', period: str='5d') -> pd.DataFrame:
    """
    Intervals available via yfinance: '1m', '2m', '5m', '15m', '30m', '60m', '90m'

    Period limit for 1-min data is usually 7 days

    5-min allows for up to 60 days, but Yahoo may cap it to 30 in practice

    Market is only open from 9:30 AM to 4:00 PM ET — make sure to trim if needed later
    """
    try:
        data = yf.download(
            tickers=name,
            interval=interval,
            period=period,
            progress=False
        )

        if data.empty:
            raise ValueError(f"No data returned for {name} with interval={interval}, period={period}")

        data = data.reset_index()
        return data

    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {name}: {e}")
        return pd.DataFrame()