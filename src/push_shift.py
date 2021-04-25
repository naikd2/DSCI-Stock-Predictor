import requests

q='GE' # Search Term
after='1606798800'
before='1609390800'
subreddit='wallstreetbets'
url = f'https://api.pushshift.io/reddit/search/submission/?q={q}&after={after}&before={before}&subreddit={subreddit}&author=&aggs=&metadata=true&frequency=hour&advanced=false&sort=desc&domain=&sort_type=num_comments&size=10000'

r = requests.get(url)

submissions = r.json()
links = {}
for s in submissions['data'][:5]:
    # get link_id
    link_id = s['permalink'].split('/')[4]
    url = f'https://api.pushshift.io/reddit/comment/search/?link_id={link_id}&limit=20000'
    r = requests.get(url)
    links[link_id] = r.json()

print(links)