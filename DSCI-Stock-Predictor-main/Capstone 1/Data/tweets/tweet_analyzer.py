import pandas as pd


df = pd.read_csv('all_tweets.csv')

df = df[['ticker','date','tweet_count','likes','retweets','open','close','volume']]
print(df.head(10))