from plotnine import *
from mizani.formatters import percent_format
from .utils import scrap_from_prices

def price_plot(prices, multi=False):
    if multi:
        start_year, end_year, ticker = scrap_from_prices(prices, multi=True)
    else:
        start_year, end_year, ticker = scrap_from_prices(prices)

    plot_title = f"{ticker} stock prices from {start_year} to {end_year}"

    plot = (
        ggplot(prices, aes(x="Date", y="Adjusted", color="Ticker")) +
        geom_line() +
        labs(title=plot_title)
    )

    fig = plot.draw()
    fig.show()


def returns_plot(returns, multi = False):
    if multi:
        start_year, end_year, ticker = scrap_from_prices(returns, multi=True)
    else:
        start_year, end_year, ticker = scrap_from_prices(returns)
    plot_title = f"Distribution of daily {ticker} stock returns from {start_year} to {end_year}"

    quantile_05 = returns["Returns"].quantile(0.05)

    returns_figure = ( ggplot(returns, aes(x="Returns")) + geom_histogram(bins=100) + geom_vline(aes(xintercept=quantile_05),
    linetype = "dashed") +
    labs(x = "", y = "",
    title = plot_title) +
    scale_x_continuous(labels=percent_format()) )

    fig = returns_figure.draw()
    fig.show()


def trading_volume_plot(trading_volume, persistence = False, multi = False):
    if multi:
        start_year, end_year, ticker = scrap_from_prices(trading_volume, multi=True)
    else:
        start_year, end_year, ticker = scrap_from_prices(trading_volume)
    if persistence:
        plot_title = f"Persistence in daily trading volume of {ticker} from {start_year} to {end_year}"
        trading_volume_figure = (
                ggplot(trading_volume, aes(x="Trading_volume_lag", y="Trading_volume", color="Ticker")) +
                geom_point() +
                geom_abline(intercept=0, slope=1, linetype="dashed") +
                labs(x="Previous day aggregate trading volume", y="Aggregate trading volume", title=plot_title)
        )
    else:
        plot_title = f"Daily trading volume of {ticker} from {start_year} to {end_year}"
        trading_volume_figure = (
                ggplot(trading_volume, aes(x="Date", y="Trading_volume", color="Ticker")) +
                geom_line() +
                labs(x="", y="Trading Volume", title=plot_title) +
                scale_x_datetime(date_breaks="5 years", date_labels="%Y")
        )

    fig = trading_volume_figure.draw()
    fig.show()
