import pandas as pd
import pandas_datareader as pdr
from .utils import current_date


def fetch_fama_french(name: str, start="1960-01-01", end=current_date()):
    """Fetch Fama-French data from the 'famafrench' source."""
    return pdr.DataReader(name=name, data_source="famafrench", start=start, end=end)[0]


def process_ff_data(data):
    """Process Fama-French factor data by converting percentages and handling dates."""
    return (
        data.divide(100)
        .reset_index()
        .assign(month=lambda x: x["Date"].dt.to_timestamp())  # Convert Period to Timestamp
        .rename(str.lower, axis="columns")
        .rename(columns={"mkt-rf": "mkt_excess"})
    )


def process_daily_ff_data(data):
    """Process daily Fama-French 3-factor data (date column instead of period)."""
    return (
        data.divide(100)
        .reset_index(names="date")
        .rename(str.lower, axis="columns")
        .rename(columns={"mkt-rf": "mkt_excess"})
    )


def process_industry_data(data):
    """Process industry portfolio data (monthly periods)."""
    return (
        data.divide(100)
        .reset_index()
        .assign(month=lambda x: x["Date"].dt.to_timestamp())  # Convert Period to Timestamp
        .rename(str.lower, axis="columns")
    )


def fetch_q_factors(start="1960-01-01", end=current_date()):
    """Fetch and process Q-factor model data."""
    factors_q_monthly_link = (
        "https://global-q.org/uploads/1/2/2/6/122679606/q5_factors_monthly_2022.csv"
    )

    factors_q_monthly = (
        pd.read_csv(factors_q_monthly_link)
        .assign(
            month=lambda x: pd.to_datetime(
                x["year"].astype(str) + "-" + x["month"].astype(str) + "-01"
            )
        )
        .drop(columns=["R_F", "R_MKT", "year"])
        .rename(columns=lambda x: x.replace("R_", "").lower())
        .query(f"month >= '{start}' and month <= '{end}'")
        .assign(**{col: lambda x: x[col] / 100 for col in ["me", "ia", "roe", "eg"]})
    )

    return factors_q_monthly


def fetch_cpi_data(start_date="1960-01-01", end_date=current_date()):
    """Fetch and process CPI data."""
    cpi_monthly = (
        pdr.DataReader(
            name="CPIAUCNS",
            data_source="fred",
            start=start_date,
            end=end_date
        )
        .reset_index(names="month")
        .rename(columns={"CPIAUCNS": "cpi"})
        .assign(cpi=lambda x: x["cpi"] / x["cpi"].iloc[-1])  # Normalize CPI data
    )
    return cpi_monthly
