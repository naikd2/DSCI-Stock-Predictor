import time

from calendar import monthrange

from data_acquisition.file_service import FileService
from data_acquisition.reddit_service import RedditService

def get_dates(year:int, month:int):
    m = ['{:04d}-{:02d}-{:02d}'.format(year, month, d)
            for d in range(1, monthrange(year, month)[1] + 1)]
    m_plus_1 = (month+1)%12
    m_plus_1 = ['{:04d}-{:02d}-{:02d}'.format(year, m_plus_1, d)
            for d in range(1, monthrange(year, m_plus_1)[1] + 1)]
    m.append(m_plus_1[0])
    return m


ticker = 'NVDA'
subreddit = 'wallstreetbets'
file_path = f"{subreddit}"
dates = []
dates.extend(get_dates(2021, 1))
dates.extend(get_dates(2021, 2))
dates.extend(get_dates(2021, 3))
dates.extend(get_dates(2021, 4))

reddit = RedditService(ticker, subreddit)
fs = FileService()

for r in range(len(dates)-1):
    start = dates[r]
    end = dates[r + 1]

    if fs.file_exists(f"{file_path}/{start}.json"):
        print(f"Skipping Posts: {start}-{end}")
        continue

    print(f"Acquiring Posts: {start}-{end}")
    posts = reddit.get_posts(start, end)
    comments = reddit.get_comments(posts)
    data = reddit.merge_data(posts, comments)

    fs.save_file(data, f"{file_path}/{start}.json")
    time.sleep(1.25) # API has rate limit
