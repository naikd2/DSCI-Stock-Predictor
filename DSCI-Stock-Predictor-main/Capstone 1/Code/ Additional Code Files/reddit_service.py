from datetime import datetime
import requests


class RedditService:
    POSTS_URL = 'https://api.pushshift.io/reddit/search/submission/'
    COMMENTS_URL = 'https://api.pushshift.io/reddit/comment/search/'

    # reddit.start_date.timestamp()
    def __init__(self, ticker, subreddit):
        self.ticker = ticker
        self.subreddit = subreddit

    def get_posts(self, start_date, end_date):
        self.start_date = datetime.fromisoformat(start_date).timestamp()
        self.end_date = datetime.fromisoformat(end_date).timestamp()

        query = {'q': self.ticker,
                 'after': "{:.0f}".format(self.start_date),
                 'before': "{:.0f}".format(self.end_date),
                 'subreddit': self.subreddit,
                 'metadata': 'true',
                 'size': 500}

        r = requests.get(f"{self.POSTS_URL}", params=query)
        return r.json()

    def get_comments(self, posts):
        links = []
        for s in posts['data']:
            links.append(s['permalink'].split('/')[4])
        if not links:
            return {}
        query = {'link_id': ",".join(links),
                 'sort_type': 'score', 'sort': 'asc',
                 'metadata': 'true', 'limit': 500}
        r = requests.get(f"{self.COMMENTS_URL}", params=query)
        return r.json()

    def merge_data(self, posts, comments):
        return {
            'posts': posts.get('data', []),
            'comments': comments.get('data', [])
        }