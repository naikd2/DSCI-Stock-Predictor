import json
import re
import pandas as pd
import emoji
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer


ps = PorterStemmer()

progress = {
    "key": 0
}

def get_progress():
    p = progress['key'] + 1
    progress['key'] = p
    return p

HASHTAG = re.compile(r'#\w*')
CASHTAG = re.compile(r'\$\w*')
MENTION = re.compile(r'@\w*')
TWITTER_WORDS = re.compile(r'\b(?<![@#])(RT|FAV)\b')
URL = re.compile(r'http\S+')
HTML_CHAR = re.compile(r'&\w*;')
STOP_WORDS = stopwords.words("english")

def clean_tweets(data, top=20):
    p = get_progress()
    tweets = json.loads(data)
    top_tweets = sorted(tweets,
                        key=lambda k: k['public_metrics']['like_count'] + k['public_metrics']['retweet_count'],
                        reverse=True)
    cleaned_tweets = []
    for t in top_tweets[:top]:
        tweet = t['text']
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

        cleaned_tweets.append(tweet)
    print((p/832) * 100)

    return ''.join(cleaned_tweets)


def preprocess(reprocess=False, top=20):
    if reprocess:
        df = pd.read_csv('all_tweets.csv')
        # Drop dates that aren't business dates
        df = df[~pd.isna(df.direction)].reset_index(drop=True)

        df['tweets'] = df.apply(lambda x: clean_tweets(x['tweets'], top=top), axis=1)

        df.to_csv('cleaned_tweets.csv')
        # clean tweets
        return df
    else:
        df = pd.read_csv('cleaned_tweets.csv')
        return df


def tfidf(df):
    tweets = df['tweets'].to_list()
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    tfidf = tfidfvectorizer.fit_transform(tweets)
    features = []
    for row in range(df.shape[0]):
        features.append(pd.DataFrame(tfidf[row].T.todense(), columns=["tfidf"]).T)
    df_tfidf = pd.concat(features).reset_index()
    df = df[['ticker', 'date', 'tweet_count', 'likes', 'retweets', 'open', 'close','volume', 'direction',
             'direction_1',
             'direction_3',
             'direction_5',
             'direction_7',
             'direction_14',
             'direction_21',
             'direction_28',
             ]]
    df = pd.concat([df, df_tfidf], axis=1)
    df.to_csv('final_dataset_tfidf.csv')

if __name__ == '__main__':
    df = preprocess(True)
    tfidf(df)

