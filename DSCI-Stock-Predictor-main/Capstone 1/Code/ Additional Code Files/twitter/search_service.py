import time
import urllib

import yaml
import datetime
import requests


class SearchService():

    def __init__(self):
        self.auth = self.__load_creds()
        self.headers = {"Authorization": f"Bearer {self.auth}"}
        self.fields = "attachments,author_id,conversation_id,created_at,id,lang,public_metrics"


    def search(self, query:str, start_time:str, end_time:str, max_results:int=10):
        cap = max_results
        if cap > 500:
            max_results = 500
        else:
            max_results = cap
        start_time = datetime.datetime.fromisoformat(start_time).astimezone().isoformat()
        end_time = datetime.datetime.fromisoformat(end_time).astimezone().isoformat()
        query = urllib.parse.urlencode({'query': f'(${query}) lang:en'})
        url = f"https://api.twitter.com/2/tweets/search/all?{query}&start_time={start_time}" \
              f"&end_time={end_time}&max_results={max_results}&tweet.fields={self.fields}"
        tweets = self.call_endpoint(url, cap)
        # &next_token = b26v89c19zqg8o3fobd8v73egzbdt3qao235oql
        # public_metrics
        # tweet_fields = ""

        return tweets


    def call_endpoint(self, url, cap):
        # CAPS TO ONLY 7500 tweets per time period
        tweets = []
        print(f"----finding max tweets {cap}")
        response = requests.get(url, headers=self.headers).json()
        tweets.extend(response['data'])
        next_token = response['meta'].get('next_token', None)
        while True:
            if len(tweets) >= cap or not next_token:
                break
            time.sleep(3.1) # Wait 3 seconds. Max of 300 calls per 15 mins
            response = requests.get(f"{url}&next_token={next_token}", headers=self.headers).json()
            tweets.extend(response['data'])
            next_token = response['meta'].get('next_token', None)
        print(f"----found tweets {len(tweets)}")
        return tweets

    def __load_creds(self):
        with open('creds.yaml') as f:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            creds = yaml.load(f, Loader=yaml.FullLoader)
            return creds['TOKEN']


