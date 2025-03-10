import pandas as pd
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