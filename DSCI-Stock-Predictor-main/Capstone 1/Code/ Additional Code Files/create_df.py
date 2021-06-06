import pandas as pd
from pathlib import Path
import json
import os
from collections import Counter

from data_acquisition.sentiment_service import SentimentService

sentimentService = SentimentService()
# create dataframe for each date and build if post and comments


def dire(close, open):
    x = close - open
    if x > 0:
        return 1 #"up"
    elif x < 0:
        return -1 #"down"
    else:
        return 0 #"none"

def main():
    # Change Ticker
    prices = pd.read_csv("data/NVDA/NVDA.csv").set_index('Date')
    prices['direction'] = prices.apply(lambda x: dire(x['Close'], x['Open']), axis=1)

    base_path = "data/NVDA/wallstreetbets"
    path = Path(base_path)

    data = {}
    for f in path.absolute().iterdir():
        k, v = load_file(f)
        data[k] = v

    df = pd.DataFrame.from_dict(data).T
    df = df.merge(prices, left_index=True, right_index=True)
    df = df[['comments', 'posts', 'direction']]
    df.to_csv('final_nvda.csv')


def load_file(file):
    date = file.stem
    with open(file.absolute(), 'r') as fp:
        d = json.load(fp)

        comments = [sentimentService.assign(c.get('body', '')) for c in d['comments']]
        posts = [sentimentService.assign(p.get('selftext', '')) for p in d['posts']]

        comments = next(iter(Counter(comments).most_common(1)), ("n/a", 0))
        posts = next(iter(Counter(posts).most_common(1)), ("n/a", 0))
        summary = {
            'comments': comments[0],
            'posts': posts[0]
        }
        return date, summary

if __name__ == '__main__':
    main()