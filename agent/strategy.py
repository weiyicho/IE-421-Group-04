import openai
import pandas as pd
import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="nvidia/llama-3.1-nemotron-70b-instruct",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key= os.getenv("NVIDIA_API_KEY"),
    temperature=0.5,
)

# Prompt to generate a backtesting.py-compatible strategy
strategy_prompt = PromptTemplate.from_template("""
You are a highly skilled and compeptive quantitative trading developer with a strong background in algorithmic trading and machine learning.
                                               


Create a **profitable intraday trading strategy** for the U.S. stock {ticker}, using the provided csv of OHLCV data.

First, analyze the data and identify potential patterns or trends that could be exploited for profit.

                                               
Instructions:
1. Write a short explanation of your trading logic and rationale.
2. Then provide a full Python class that inherits from `backtesting.Strategy`, using:
   - `init(self)` for indicator setup
   - `next(self)` for trade logic

Assume these imports are already provided:
```python
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
Return only:
A description of the strategy and the correspondingPython code inside a python ... block """)

chain = strategy_prompt | llm

def generate_strategy(df, user_prompt="Come up with a profitable strategy on SPY"): 
    # Extract ticker symbol from user prompt
    print(f"[INFO] Analyzing data for strategy generation...")
    if "on" in user_prompt:
        ticker = user_prompt.split("on")[-1].strip().upper()
    else:
        ticker = "SPY"

    try:
        # Run Langchain chain
        print(f"[INFO] Building strategy for {ticker}...")
        response = chain.invoke({"ticker": ticker})
        text = response["text"] if isinstance(response, dict) else str(response)

        if "```" in text:
            parts = text.split("```")
            description = parts[0].strip()
            code_block = next((part for part in parts if "class" in part), "# No valid strategy code returned")
            code = code_block.replace("python", "").strip()
        else:
            description = text.strip()
            code = "# No code block returned by LLM."
        print(f"[INFO] Strategy built!")
        return code, description

    except Exception as e:
        print(f"[ERROR] LLM strategy generation failed: {e}")
        return "# LLM generation error", "Strategy generation failed."