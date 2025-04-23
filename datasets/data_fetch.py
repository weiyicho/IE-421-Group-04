# Fetch data
import yfinance as yf
from datetime import datetime

def fetch_data(ticker="AAPL", start="2018-01-01", end=None):
    end = end or datetime.today().strftime('%Y-%m-%d')
    return yf.download(ticker, start=start, end=end)