import stanza
import pandas as pd
import json
import emoji
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer


ps = PorterStemmer()


sentiment_mapping = {
    0: "negative",
    1: "neutral",
    2: "positive",
    "key": 0
}

HASHTAG = re.compile(r'#\w*')
CASHTAG = re.compile(r'\$\w*')
MENTION = re.compile(r'@\w*')
TWITTER_WORDS = re.compile(r'\b(?<![@#])(RT|FAV)\b')
URL = re.compile(r'http\S+')
HTML_CHAR = re.compile(r'&\w*;')
STOP_WORDS = stopwords.words("english")

def get_progress():
    progress = sentiment_mapping['key'] + 1
    sentiment_mapping['key'] = progress
    return progress

def create_sentiments(x, size, limit=20, type='postive'):
    # CREATE FEATURES FOR BUY OR SELL as predictors
    progress = get_progress()
    tweets = json.loads(x)
    sentiment_for_the_day = []
    top_tweets = sorted(tweets,
                        key=lambda k: k['public_metrics']['like_count'] + k['public_metrics']['retweet_count'],
                        reverse=True)

    for tweet in top_tweets[:limit]: # limit per day
        tweet = tweet['text']
        tweet = HTML_CHAR.sub('', tweet)
        tweet = HASHTAG.sub('', tweet) # remove hashtags
        tweet = CASHTAG.sub('', tweet) # remove cashtags
        tweet = MENTION.sub('', tweet) # remove mentions
        tweet = TWITTER_WORDS.sub('', tweet) # remove reserved words
        tweet = URL.sub('', tweet) # remove urls
        tweet = emoji.demojize(tweet) # convert emoji to words
        tweet = tweet.lower()
        tweet = ' '.join([w for w in tweet.split() if w not in STOP_WORDS])
        tweet = ' '.join([ps.stem(word) for word in word_tokenize(tweet) if word.isalpha()])
        try:
            doc = nlp(tweet)
            sentiment = [s.sentiment for s in doc.sentences][0]
        except Exception as e:
            sentiment = 0
        sentiment_for_the_day.append(sentiment)

    print((progress/size) * 100)
    if type == 'negative':
        return sentiment_for_the_day.count(0)/limit
    elif type == 'neutral':
        return sentiment_for_the_day.count(1) /limit
    elif type == 'positive':
        return sentiment_for_the_day.count(2) /limit
    else:
        raise ValueError


# stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize,sentiment')

df = pd.read_csv('all_tweets.csv')
size = len(df)

progress = 0
df['sentiment_negative'] = df.apply(lambda x: create_sentiments(x['tweets'], size, type='negative'), axis=1)
df['sentiment_neutral'] = df.apply(lambda x: create_sentiments(x['tweets'], size, type='neutral'), axis=1)
df['sentiment_postive'] = df.apply(lambda x: create_sentiments(x['tweets'], size, type='positive'), axis=1)
df = df[['ticker', 'date', 'tweet_count', 'likes', 'retweets',
         'open', 'close', 'volume', 'direction',
            'direction_1',
            'direction_3',
            'direction_5',
            'direction_7',
            'direction_14',
            'direction_21',
            'direction_28',
         'sentiment_negative', 'sentiment_neutral', 'sentiment_postive']]

df.to_csv("final_dataset_sentiment.csv")
