from pathlib import Path
import json
import pandas as pd
import yfinance as yf

WINDOWS = [1, 3, 5, 7, 14, 21, 28]


def load_file(file):
    date = file.stem
    with open(file.absolute(), 'r') as fp:
        tweets = json.load(fp)

    return date, tweets


def load_finance(ticker) -> pd.DataFrame:
    tkr = yf.Ticker(ticker)
    hist = tkr.history(start='2020-05-01', end='2021-04-30')
    return calculate_rolling_average(hist)


def calculate_rolling_average(stocks):
    # stocks.rolling(2, min_periods=1).sum()
    for window in WINDOWS:
        stocks[f'close_avg_{window}_days'] = stocks['Close'].rolling(window, win_type='blackman').mean()
    for window in WINDOWS:
        stocks[f'open_avg_{window}_days'] = stocks['Open'].rolling(window, win_type='blackman').mean()
    return stocks


def dire(close, open):
    x = close - open
    if x > 0:
        return 1 #"up"
    elif x < 0:
        return -1 #"down"
    else:
        return 0 #"none"

def load_ticker(ticker):

    stock_data = load_finance(ticker)
    path_twitter = Path(ticker)
    dataset = []
    for f in path_twitter.absolute().iterdir():
        date, tweets = load_file(f)
        try:
            yahoo = stock_data.loc[date]
            open = yahoo.get('Open')
            close = yahoo.get('Close')
            direction = dire(close, open)
            volume = yahoo.get('Volume')
            window_direction = {}
            for w in WINDOWS:
                window_direction[str(w)] = dire(yahoo.get(f'close_avg_{w}_days'), yahoo.get(f'open_avg_{w}_days'))
        except KeyError:
            open = 'N/A'
            close = 'N/A'
            direction = 'N/A'
            volume = 'N/A'
            window_direction = {}
        dataset.append({
            'ticker': ticker,
            'date': date,
            'tweets': json.dumps(tweets),
            'tweet_count': len(tweets),
            'likes': sum([t['public_metrics']['like_count'] for t in tweets]),
            'retweets': sum([t['public_metrics']['retweet_count'] for t in tweets]),
            'open': open,
            'close': close,
            'volume': volume,
            'direction': direction,
            'direction_1': window_direction.get('1', 'N/A'),
            'direction_3': window_direction.get('3', 'N/A'),
            'direction_5': window_direction.get('5', 'N/A'),
            'direction_7': window_direction.get('7', 'N/A'),
            'direction_14': window_direction.get('14', 'N/A'),
            'direction_21': window_direction.get('21', 'N/A'),
            'direction_28': window_direction.get('28', 'N/A')
        })
    return dataset

if __name__ == '__main__':
    tickers = ["AMD", "GE", "NVDA", "TSLA"]
    all_tickers = []
    for t in tickers:
        all_tickers.extend(load_ticker(t))
    df = pd.DataFrame.from_records(all_tickers)
    df.to_csv("all_tweets.csv", index=False)

    df = df[['ticker', 'date', 'tweet_count', 'likes', 'retweets', 'direction']]

