# FinAnalysis

FinAnalysis is a Python package for fetching, analyzing, and visualizing stock price data using Yahoo Finance.

## Features
- Fetch stock price data using Yahoo Finance.
- Compute stock returns and their statistics.
- Generate plots for stock prices, returns distributions, and trading volume.

## Installation
Install required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure
```
finanalysis/
│── __init__.py         # Package initialization
│── analysis.py         # Functions for analyzing stock data
│── data_proccesing.py  # (Possibly misspelled) Data processing functions
│── plot.py             # Visualization functions using plotnine
│── request_data.py     # Fetch stock data from Yahoo Finance
│── utils.py            # Utility functions
main.py                 # Example script to run analysis
requirements.txt        # List of dependencies
```

## Usage
Run the main script to fetch and analyze Apple stock (AAPL):
```bash
python main.py
```
## License
This project is licensed under the MIT License.

