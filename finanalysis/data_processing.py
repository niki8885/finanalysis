import numpy as np
import pandas as pd
from .fin_data import *


def calculate_log_returns(prices):
    if "Returns" not in prices or prices["Returns"].isnull().all():
        raise ValueError("Input data is empty or the 'Returns' column is missing.")

    if (prices["Returns"] <= -1).any():
        raise ValueError("Invalid values in 'Returns' column: some returns are ≤ -100%. Log cannot be computed.")
    prices["Log_returns"] = np.log(1 + prices["Returns"])

    prices.dropna(subset=["Log_returns"], inplace=True)

    return prices


def calculate_trading_volume(prices, multi=False):
    trading_volume = (
        prices
        .assign(Trading_volume=lambda x: (x["Volume"] * x["Adjusted"]) / 1e9)
        .groupby(["Date", "Ticker"], as_index=False)
        .agg({"Trading_volume": "sum"})
        .assign(Trading_volume_lag=lambda x: x["Trading_volume"].shift(periods=1))
    )

    if not multi:
        trading_volume["Ticker"] = prices["Ticker"].iloc[0]

    return trading_volume


def merge_month_data(prices, start="1960-01-01", end=current_date()):
    """
    Merge monthly factor data with daily price data and return price on a specific day (e.g., first day of the month).

    Parameters:
    - prices: DataFrame containing price data with a 'Date' column.
    - start: start date for the data to be fetched.
    - end: end date for the data to be fetched.

    Returns:
    - Merged DataFrame with monthly factors and the price of the first day of each month.
    """
    # Fetching and processing Fama-French and other factor data
    factors_ff3_monthly = process_ff_data(
        fetch_fama_french("F-F_Research_Data_Factors", start, end))
    factors_ff5_monthly = process_ff_data(
        fetch_fama_french("F-F_Research_Data_5_Factors_2x3", start, end))
    industries_ff_monthly = process_industry_data(
        fetch_fama_french("10_Industry_Portfolios", start, end))
    factors_q_monthly = fetch_q_factors(start, end)
    cpi_data = fetch_cpi_data()  # Assuming this function exists in your module

    # Ensure 'Date' column is converted to datetime if necessary
    prices['Date'] = pd.to_datetime(prices['Date'], errors='coerce')

    # Extract the first price of each month (based on the 'Open' column)
    monthly_prices = (
        prices.groupby(prices['Date'].dt.to_period('M'))  # Group by month
        .first()  # Get the first trading day of the month
        .reset_index(drop=True)
    )

    # Rename columns to avoid conflicts during merge
    monthly_prices.rename(columns={'Date': 'Date_price'}, inplace=True)
    factors_q_monthly.rename(columns={'month': 'month_factor'}, inplace=True)

    # Rename the 'month' column in CPI data to avoid conflict during merge
    cpi_data.rename(columns={'month': 'month_cpi'}, inplace=True)

    # Merge the price data with the Fama-French and other factors data
    merged_data = pd.merge(monthly_prices, factors_ff3_monthly, left_on="Date_price", right_on="month", how="inner")
    merged_data = pd.merge(merged_data, factors_ff5_monthly, left_on="Date_price", right_on="month", how="inner")
    merged_data = pd.merge(merged_data, industries_ff_monthly, left_on="Date_price", right_on="month", how="inner")
    merged_data = pd.merge(merged_data, factors_q_monthly, left_on="Date_price", right_on="month_factor", how="inner")
    merged_data = pd.merge(merged_data, cpi_data, left_on="Date_price", right_on="month_cpi", how="left")

    # Return the final merged DataFrame
    return merged_data
