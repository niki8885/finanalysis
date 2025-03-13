# FinAnalysis

FinAnalysis is a Python package designed to fetch, analyze, and visualize stock price data using Yahoo Finance and other financial datasets.

## Features
- Fetch stock price data from Yahoo Finance.
- Compute stock returns and their statistics.
- Generate plots for stock prices, returns distributions, and trading volume.
- Fetch and process Fama-French, Q-Factor, and CPI data.
- Merge financial factors with stock data for deeper analysis.

## Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
finanalysis/
│── __init__.py            # Package initialization
│── analysis.py            # Functions for analyzing stock data, including MVP calculations
│── data_processing.py     # Data processing functions (e.g., merge monthly factor data)
│── plot.py                # Visualization functions using plotnine
│── request_data.py        # Fetch stock data from Yahoo Finance and external sources
│── fin_data.py            # Fetch and process Fama-French, Q-Factor, and CPI data
│── utils.py               # Utility functions
main.py                    # Example script to run analysis
requirements.txt           # List of dependencies
```

## Usage
Run the main script to fetch and analyze Apple stock (AAPL):
```bash
python main.py
```

## Key Functions
- **`fetch_fama_french()`**: Fetch Fama-French data from an external source.
- **`process_ff_data()`**: Process monthly Fama-French data.
- **`process_daily_ff_data()`**: Process daily Fama-French data.
- **`fetch_q_factors()`**: Fetch and process Q-factor data.
- **`fetch_cpi_data()`**: Fetch and process Consumer Price Index (CPI) data.
- **`merge_month_data()`**: Merge monthly financial factor data with daily price data.
- **`compute_mvp_statistics()`**: Calculate the Minimum Variance Portfolio (MVP) statistics, including expected return and volatility.

## License
This project is licensed under the MIT License.