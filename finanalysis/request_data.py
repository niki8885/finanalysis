import numpy as np
import pandas as pd
import yfinance as yf
from .utils import current_date

def request_prices(ticker,start_date,end_date = current_date(), returns = True):
    prices = yf.download(
        tickers = ticker,
        start = start_date,
        end= end_date,
        progress=False,
        auto_adjust=False
    ).reset_index()

    if prices.empty:
        return None

    if isinstance(prices.columns, pd.MultiIndex):
        prices.columns = [' '.join(col).strip() for col in prices.columns]

    rename_dict = {
        "Date": "Date",
        f"Open {ticker}": "Open",
        f"High {ticker}": "High",
        f"Low {ticker}": "Low",
        f"Close {ticker}": "Close",
        f"Adj Close {ticker}": "Adjusted",
        f"Volume {ticker}": "Volume"
    }

    prices = prices.rename(columns=rename_dict)

    prices["Date"] = pd.to_datetime(prices["Date"])
    prices["Adjusted"] = prices["Adjusted"].astype(float)
    prices["Ticker"] = ticker

    if returns:
        prices_returns = (
            prices
            .sort_values("Date")
            .assign(Returns=lambda x: x["Adjusted"].pct_change())
            .loc[:, ["Date","Ticker" ,"Open", "High", "Low", "Close", "Adjusted", "Returns", "Volume"]]
        )
        return prices_returns
    else:
        return prices


