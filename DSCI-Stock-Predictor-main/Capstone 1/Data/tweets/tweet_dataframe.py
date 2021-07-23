from pathlib import Path
import json
import pandas as pd

def load_file(file):
    date = file.stem
    with open(file.absolute(), 'r') as fp:
        tweets = json.load(fp)

    return date, tweets

def load_finance(file):
    yahoo = pd.read_csv(file)
    return yahoo.set_index("Date")

def dire(close, open):
    x = close - open
    if x > 0:
        return 1 #"up"
    elif x < 0:
        return -1 #"down"
    else:
        return 0 #"none"

def load_ticker(ticker):

    path_yahoo = Path(f"{ticker}.csv").absolute()
    stock_data = load_finance(path_yahoo)
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
        except KeyError:
            open = 'N/A'
            close = 'N/A'
            direction = 'N/A'
            volume = 'N/A'

        dataset.append({
            'ticker': ticker,
            'date': date,
            'tweets': tweets,
            'tweet_count': len(tweets),
            'likes': sum([t['public_metrics']['like_count'] for t in tweets]),
            'retweets': sum([t['public_metrics']['retweet_count'] for t in tweets]),
            'open': open,
            'close': close,
            'direction': direction,
            'volume': volume
        })
    return dataset

if __name__ == '__main__':
    tickers = ["AMD", "GE", "NVDA", "TSLA"]
    all_tickers = []
    for t in tickers:
        all_tickers.extend(load_ticker(t))
    df = pd.DataFrame.from_records(all_tickers)
    df.to_csv("all_tweets.csv")

    df = df[['ticker', 'date', 'tweet_count', 'likes', 'retweets', 'direction']]
    df.to_csv("sample_tweets.csv", index=False)