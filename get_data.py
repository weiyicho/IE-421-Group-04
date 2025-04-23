import yfinance as yf
import pandas as pd

def fetch_data(interval, period, ticker_symbol):
    try:
        data = yf.download(tickers=ticker_symbol, period=period, interval=interval)
    except Exception as e:
        print("Error Occurred:", str(e))
        data = pd.DataFrame()
        data.columns = ['Date','Close', 'High', 'Low', 'Open','Volume']
    return data
