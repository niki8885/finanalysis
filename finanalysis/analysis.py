import pandas as pd

def returns_statistics(returns,decimal = 3, method = 'total'):
    if method == 'total':
        print(pd.DataFrame(returns["Returns"].describe()).round(decimal).T)
    elif method == 'by year':
        print(returns["Returns"].groupby(returns["Date"].dt.year).describe().round(decimal))