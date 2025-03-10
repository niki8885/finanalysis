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

finanalysis.trading_volume_plot(trade_volume)
finanalysis.trading_volume_plot(trade_volume, persistence = True)

tickers = ["AAPL","MS"]
start_date = "2020-01-01"
prices = finanalysis.request_multi_prices(tickers, start_date)
print(prices)
finanalysis.multiple_returns_statistics(prices)
finanalysis.returns_plot(prices, multi=True)
finanalysis.price_plot(prices,multi=True)
trade_volume = finanalysis.calculate_trading_volume(prices, multi=True)

print(trade_volume)

finanalysis.trading_volume_plot(trade_volume, persistence = False, multi=True)
finanalysis.trading_volume_plot(trade_volume, persistence = True, multi=True)