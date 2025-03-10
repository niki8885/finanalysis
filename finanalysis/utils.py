from datetime import datetime


def current_date():
    today = datetime.today().date()
    return today


def scrap_from_prices(prices):
    start_year = prices["Date"].min().year
    end_year = prices["Date"].max().year
    ticker = prices["Ticker"].iloc[0]
    return start_year,end_year,ticker