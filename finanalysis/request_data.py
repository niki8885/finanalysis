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


def request_multi_prices(tickers, start_date, end_date = current_date(), returns = True):
    if not tickers:
        print("No symbols found. Skipping Yahoo Finance request.")
        return pd.DataFrame()

    prices = yf.download(
        tickers = tickers,
        start = start_date,
        end = end_date,
        progress = False,
        auto_adjust = False
    )

    prices = (prices
                    .stack(level=1, future_stack=True)
                    .reset_index()
                    .rename(columns={"level_1": "Ticker", "Date": "Date",
                                     "Close": "Close", "Open": "Open",
                                     "High": "High", "Low": "Low",
                                     "Adj Close": "Adjusted", "Volume": "Volume"}))

    if returns:
        prices_returns = (
            prices
            .sort_values("Date")
            .assign(Returns=lambda x: x.groupby("Ticker")["Adjusted"].pct_change(fill_method=None))
            .loc[:, ["Date", "Ticker", "Open", "High", "Low", "Close", "Adjusted", "Returns", "Volume"]]
            .dropna(subset=["Returns"])
        )
        return prices_returns
    else:
        return prices