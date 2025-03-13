import pandas as pd
import numpy as np
from .utils import scrap_from_prices

def returns_statistics(returns, decimal=3, method='total'):
    start_year, end_year, ticker = scrap_from_prices(returns)
    print(f"Returns statistics for {ticker} from {start_year} to {end_year}")

    if method == 'total':
        print("\nTotal Statistics:")
        total_stats = pd.DataFrame(returns["Returns"].describe()).round(decimal).T
        print(total_stats)

    elif method == 'by year':
        # Print yearly statistics
        print("\nYearly Statistics:")
        yearly_stats = returns["Returns"].groupby(returns["Date"].dt.year).describe().round(decimal)
        print(yearly_stats)

def multiple_returns_statistics(returns, decimal=3):
    start_year, end_year, ticker = scrap_from_prices(returns,multi = True)
    print(f"Returns statistics for {ticker} from {start_year} to {end_year}")
    print("\nTotal Statistics:")
    print(returns.groupby("Ticker")["Returns"].describe().round(decimal))


def compute_mvp_statistics(data):
    """
    Computes the Minimum Variance Portfolio (MVP) statistics, including expected return and volatility.

    Parameters:
        data (pd.DataFrame): A DataFrame containing columns ["Ticker", "Date", "Adjusted"].

    Returns:
        pd.DataFrame: A DataFrame with the computed average return and volatility.
    """

    # Validate input
    required_columns = {"Ticker", "Date", "Adjusted"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Input data must contain the following columns: {required_columns}")

    # Filter and clean data
    prices = (
        data.groupby("Ticker")
        .apply(lambda x: x.assign(counts=x["Adjusted"].dropna().count()))
        .reset_index(drop=True)
        .query("counts == counts.max()")
    )

    print(f"Filtered tickers with max data points: {prices['Ticker'].nunique()} assets")

    # Compute monthly returns
    returns_matrix = (
        prices.pivot(columns="Ticker", values="Adjusted", index="Date")
        .resample("M").last()  # Use "M" instead of "m" (case-sensitive)
        .pct_change()
        .dropna()
    )

    print(f"Monthly returns matrix shape: {returns_matrix.shape}")

    # Compute expected returns and covariance matrix
    mu = np.array(returns_matrix.mean()).T
    sigma = np.array(returns_matrix.cov())
    N = returns_matrix.shape[1]
    iota = np.ones(N)

    # Compute MVP weights
    sigma_inv = np.linalg.inv(sigma)
    mvp_weights = sigma_inv @ iota
    mvp_weights = mvp_weights / mvp_weights.sum()

    # Compute MVP return and volatility
    mvp_return = mu.T @ mvp_weights
    mvp_volatility = np.sqrt(mvp_weights.T @ sigma @ mvp_weights)

    mvp_moments = pd.DataFrame({"Value": [mvp_return, mvp_volatility]},
                               index=["Average Return", "Volatility"]).round(3)

    print("\nMinimum Variance Portfolio Statistics:")
    print(mvp_moments)

    return mvp_moments

