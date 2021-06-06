import yfinance as yf

ticker = 'NVDA'
tkr = yf.Ticker(ticker)

hist = tkr.history(start='2021-01-01', end='2021-04-30')

hist.to_csv(f"{ticker}.csv")