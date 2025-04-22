import yfinance as yf
import pandas as pd
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import initialize_agent

class ToolForModel:
    @tool
    def calculate_area(length: float, width: float) -> float:
        """Calculate the area of a rectangle given its length and width."""
        return length * width

    @tool
    def fetch_data(interval: str, period: str, ticker_symbol: str) -> pd.DataFrame:
        """Fetch historical stock data from Yahoo Finance."""
        try:
            df = yf.download(tickers=ticker_symbol, period=period, interval=interval)
        except Exception as e:
            # return empty DataFrame on error
            df = pd.DataFrame(columns=['Date','Open','High','Low','Close','Adj Close','Volume'])
        return df

tools = [
    getattr(ToolForModel, fn)
    for fn in dir(ToolForModel)
    if callable(getattr(ToolForModel, fn)) and hasattr(getattr(ToolForModel, fn), "args_schema")
]

llm = ChatOpenAI(model_name="gpt-4.1-nano")
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="openai-functions",
    verbose=True,
)

# 4) Now you can simply call
print(agent.run("What is the area of a rectangle with length 5 and width 10?"))
# → “50”

# or fetch stock data:
df = agent.run("Fetch 1mo daily data for ticker_symbol='AAPL', period='1mo', interval='1d'.")
