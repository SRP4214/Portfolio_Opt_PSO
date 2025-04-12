import yfinance as yf

def getStockReturns(tickers, startDate, end_date):
    data = yf.download(tickers, start=startDate, end=end_date, auto_adjust=False)
    # We'll consider adjusted closing prices
    adjustedClose = data['Adj Close']
    returns = adjustedClose.pct_change().dropna()
    return returns