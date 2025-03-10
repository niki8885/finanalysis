import numpy as np
import pandas as pd


def calculate_log_returns(prices):
    if "Returns" not in prices or prices["Returns"].isnull().all():
        raise ValueError("Input data is empty or the 'Returns' column is missing.")

    if (prices["Returns"] <= -1).any():
        raise ValueError("Invalid values in 'Returns' column: some returns are ≤ -100%. Log cannot be computed.")
    prices["Log_returns"] = np.log(1 + prices["Returns"])

    prices.dropna(subset=["Log_returns"], inplace=True)

    return prices


def calculate_trading_volume(prices):
    trading_volume = (
        prices
        .assign(Trading_volume=lambda x: (x["Volume"] * x["Adjusted"]) / 1e9)
        .groupby("Date", as_index=False)
        .agg({"Trading_volume": "sum"})
        .assign(Trading_volume_lag=lambda x: x["Trading_volume"].shift(periods=1))
    )
    trading_volume["Ticker"] = prices["Ticker"].iloc[0]
    return trading_volume
