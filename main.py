import finanalysis

ticker = "AAPL"
start_date = "2000-01-01"
price = finanalysis.request_prices(ticker, start_date)
price = finanalysis.calculate_log_returns(price)

finanalysis.returns_statistics(price,method = "total")
finanalysis.returns_statistics(price,method = "by year")

finanalysis.returns_plot(price)
finanalysis.price_plot(price)
trade_volume = finanalysis.calculate_trading_volume(price)
print(trade_volume)
finanalysis.trading_volume_plot(trade_volume)