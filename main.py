from lxml.html.diff import merge_delete

import finanalysis

# ticker = "AAPL"
# start_date = "2000-01-01"
# price = finanalysis.request_prices(ticker, start_date)
# price = finanalysis.calculate_log_returns(price)
# print(price)
# merged_data = finanalysis.merge_month_data(price)
# print(merged_data.tail())

# finanalysis.returns_statistics(price,method = "total")
# finanalysis.returns_statistics(price,method = "by year")
#
# finanalysis.returns_plot(price)
# finanalysis.price_plot(price)
# trade_volume = finanalysis.calculate_trading_volume(price)
#
# finanalysis.trading_volume_plot(trade_volume)
# finanalysis.trading_volume_plot(trade_volume, persistence = True)

tickers = ["KO", "JPM", "NFLX", "BAC", "TMUS"]
start_date = "2020-01-01"
prices = finanalysis.request_multi_prices(tickers, start_date)
print(prices)
finanalysis.multiple_returns_statistics(prices)
finanalysis.returns_plot(prices, multi=True)
finanalysis.compute_mvp_statistics(prices)

finanalysis.price_plot(prices,multi=True)
trade_volume = finanalysis.calculate_trading_volume(prices, multi=True)

print(trade_volume)

finanalysis.trading_volume_plot(trade_volume, persistence = False, multi=True)
finanalysis.trading_volume_plot(trade_volume, persistence = True, multi=True)

# finanalysis.var(prices)
# finanalysis.var_plot(prices, multi=True)
# finanalysis.var(prices, method="parametric")
# finanalysis.var_plot(prices, method="parametric", multi=True)
finanalysis.cvar_plot(prices, multi=True)
finanalysis.cvar_plot(prices, method="parametric", multi=True)

# factors_ff3_monthly = finanalysis.process_ff_data(finanalysis.fetch_fama_french("F-F_Research_Data_Factors"))
# factors_ff5_monthly = finanalysis.process_ff_data(finanalysis.fetch_fama_french("F-F_Research_Data_5_Factors_2x3"))
# factors_ff3_daily = finanalysis.process_daily_ff_data(finanalysis.fetch_fama_french("F-F_Research_Data_Factors_daily"))
# industries_ff_monthly = finanalysis.process_industry_data(finanalysis.fetch_fama_french("10_Industry_Portfolios"))
# factors_q_monthly = finanalysis.fetch_q_factors()
# cpi_data = finanalysis.fetch_cpi_data()
