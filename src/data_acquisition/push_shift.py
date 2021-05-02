import time

import requests
import json
from calendar import monthrange

from reddit_service import RedditService

def get_dates(year:int, month:int):
    return ['{:04d}-{:02d}-{:02d}'.format(year, month, d)
            for d in range(1, monthrange(year, month)[1] + 1)]


reddit = RedditService('GE', 'wallstreetbets')

dates = get_dates(2021, 1)

for r in range(len(dates)-1):
    start = dates[r]
    end = dates[r + 1]
    print(f"Acquiring Posts: {start}-{end}")
    posts = reddit.get_posts(start, end)
    num_posts = posts['metadata']['results_returned']
    print(num_posts)
    if num_posts > 0:
        time.sleep(0.5)
        comments = reddit.get_comments(posts)
        break
    time.sleep(1) # API has rate limit
