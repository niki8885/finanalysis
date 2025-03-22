from plotnine import *
import matplotlib.pyplot as plt
from .utils import scrap_from_prices
import numpy as np
from scipy.stats import norm

def var(data, method="hist", confidence_level=0.95):
    if method == "hist":
        var_hist = data["Returns"].quantile(1 - confidence_level)
        print(f"VaR (Historical Method) at {confidence_level * 100}% confidence level: {var_hist:.4f}")
        return var_hist
    elif method == "parametric":
        mean_return = data["Returns"].mean()
        std_dev = data["Returns"].std()
        z_score = norm.ppf(1 - confidence_level)  # Z-score for given confidence level

        var_parametric = mean_return + z_score * std_dev  # Parametric VaR formula
        print(f"VaR (Parametric Method) at {confidence_level * 100}% confidence level: {var_parametric:.4f}")
        return var_parametric
    else:
        raise ValueError("Method must be 'hist' or 'parametric'.")


def cvar(data, method="hist", confidence_level=0.95):
    """Calculate Conditional Value at Risk (CVaR)"""
    var_value = var(data, method, confidence_level)

    if method == "hist":
        # Historical CVaR is the average return below the VaR
        cvar_hist = data[data["Returns"] <= var_value]["Returns"].mean()
        print(f"CVaR (Historical Method) at {confidence_level * 100}% confidence level: {cvar_hist:.4f}")
        return cvar_hist

    elif method == "parametric":
        mean_return = data["Returns"].mean()
        std_dev = data["Returns"].std()
        z_score = norm.ppf(1 - confidence_level)

        # Parametric CVaR: calculate the expected return of the tail
        # This is the expected value of the distribution for returns worse than the VaR level.
        cvar_parametric = mean_return - (std_dev * norm.pdf(z_score) / (1 - confidence_level))
        print(f"CVaR (Parametric Method) at {confidence_level * 100}% confidence level: {cvar_parametric:.4f}")
        return cvar_parametric

    else:
        raise ValueError("Method must be 'hist' or 'parametric'.")


def var_plot(data, method="hist", confidence_level=0.95, multi=False):
    var_data = var(data, method=method, confidence_level=confidence_level)
    if multi:
        start_year, end_year, ticker = scrap_from_prices(data, multi=True)
    else:
        start_year, end_year, ticker = scrap_from_prices(data)
    if method == "hist":
        plot_title = f"{ticker} Histogram of Returns \nwith VaR Level from {start_year} to {end_year} (Historical Method)"
    elif method == "parametric":
        plot_title = f"{ticker} Histogram of Returns \nwith VaR Level from {start_year} to {end_year} (Parametric Method)"
    plot = (
            ggplot(data, aes(x="Returns")) +
            geom_histogram(binwidth=0.01, fill="blue", alpha=0.7, color="black") +
            geom_vline(xintercept=var_data, color="red", linetype="dashed", size=1) +
            labs(
                title=plot_title,
                x="Returns",
                y="Frequency"
            ) +
            theme_minimal() +
            theme(
                panel_background=element_rect(fill="white"),
                plot_background=element_rect(fill="white")
            )
    )
    fig = plot.draw()
    fig.show()

def cvar_plot(data, method="hist", confidence_level=0.95, multi=False):
    cvar_data = cvar(data, method=method, confidence_level=confidence_level)
    if multi:
        start_year, end_year, ticker = scrap_from_prices(data, multi=True)
    else:
        start_year, end_year, ticker = scrap_from_prices(data)
    if method == "hist":
        plot_title = f"{ticker} Histogram of Returns \nwith CVaR Level from {start_year} to {end_year} (Historical Method)"
    elif method == "parametric":
        plot_title = f"{ticker} Histogram of Returns \nwith CVaR Level from {start_year} to {end_year} (Parametric Method)"
    plot = (
            ggplot(data, aes(x="Returns")) +
            geom_histogram(binwidth=0.01, fill="blue", alpha=0.7, color="black") +
            geom_vline(xintercept=cvar_data, color="green", linetype="dashed", size=1) +
            labs(
                title=plot_title,
                x="Returns",
                y="Frequency"
            ) +
            theme_minimal() +
            theme(
                panel_background=element_rect(fill="white"),
                plot_background=element_rect(fill="white")
            )
    )
    fig = plot.draw()
    fig.show()
