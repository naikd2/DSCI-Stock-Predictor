import stanza
import pandas as pd
import json
import emoji
from collections import Counter


sentiment_mapping = {
    0: "negative",
    1: "neutral",
    2: "positive",
    "key": 0
}

def get_progress():
    progress = sentiment_mapping['key'] + 1
    sentiment_mapping['key'] = progress
    return progress

def create_sentiments(x, size, limit=25):
    # CREATE FEATURES FOR BUY OR SELL as predictors
    progress = get_progress()
    tweets = json.loads(x)
    sentiment_for_the_day = []
    top_tweets = sorted(tweets,
                        key=lambda k: k['public_metrics']['like_count'] + k['public_metrics']['retweet_count'],
                        reverse=True)

    for tweet in top_tweets[:limit]: # limit per day
        tweet = tweet['text']
        tweet = emoji.demojize(tweet)
        doc = nlp(tweet)
        sentiment = [s.sentiment for s in doc.sentences]
        sentiment = list(filter(lambda x: x != 1, sentiment))
        # I love GE. I am buying today. Negative sentence.
        # 2, 1 , 0
        # { 33% - Positive,
        # 33% - Negative,
        # 33% - Neutral }
        try:
            sentiment = max(sentiment)
        except:
            sentiment = 1
        sentiment_for_the_day.append(sentiment)
    value, count = Counter(sentiment_for_the_day).most_common()[0]
    print((progress/size) * 100)
    return value


# stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')

df = pd.read_csv('all_tweets.csv')
size = len(df)

progress = 0
df['sentiment'] = df.apply(lambda x: create_sentiments(x['tweets'], size), axis=1)
df = df[['ticker', 'date', 'tweet_count', 'likes', 'retweets',
         'open', 'close', 'volume', 'direction', 'sentiment']]
# aggregate tweets together  - Need to remove @ and http links
# bag of words
# sentiment (percentage or one hot)
# TDIF

# df.to_csv("final_dataset.csv")
