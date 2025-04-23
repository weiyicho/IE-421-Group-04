import yfinance as yf
import pandas as pd
import os

def fetch_intraday_data(name: str="SPY", interval: str='5m', period: str='5d', use_cache: bool=True) -> pd.DataFrame:
    """
    Intervals available via yfinance: '1m', '2m', '5m', '15m', '30m', '60m', '90m'

    Period limit for 1-min data is usually 7 days

    5-min allows for up to 60 days, but Yahoo may cap it to 30 in practice

    Market is only open from 9:30 AM to 4:00 PM ET — make sure to trim if needed later
    """
    cache_dir = "data"
    os.makedirs(cache_dir, exist_ok=True)
    cache_filename = f"{name}_{interval}_{period}.csv"
    cache_path = os.path.join(cache_dir, cache_filename)

    # Try to load from cache
    if use_cache and os.path.exists(cache_path):
        try:
            print(f"[INFO] Loading cached data from {cache_path}")
            df = pd.read_csv(cache_path, parse_dates=["Datetime"])
            print(f"[INFO] Data fetched!")
            return df
        except Exception as e:
            print(f"[WARNING] Failed to read cache file, refetching: {e}")
    
    try:
        print(f"[INFO] Fetching YFinance data for {name} with interval={interval}, period={period}")
        data = yf.download(
            tickers=name,
            interval=interval,
            period=period,
            progress=False
        )

        if data.empty:
            raise ValueError(f"No data returned for {name} with interval={interval}, period={period}")


        data = data.reset_index()

        if use_cache:
            data.to_csv(cache_path, index=False)
            print(f"[INFO] Data cached to {cache_path}")
            

        return data

    except Exception as e:
        print(f"[ERROR] Failed to fetch data for {name}: {e}")
        return pd.DataFrame()