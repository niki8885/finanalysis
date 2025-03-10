from datetime import datetime


def current_date():
    today = datetime.today().date()
    return today


def scrap_from_prices(prices, multi = False):
    if multi:
        ticker = prices["Ticker"].unique()
        ticker = ', '.join(ticker.tolist())
    else:
        ticker = prices["Ticker"].iloc[0]
    start_year = prices["Date"].min().year
    end_year = prices["Date"].max().year
    return start_year,end_year,ticker