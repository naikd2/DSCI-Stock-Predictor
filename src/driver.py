import praw

client_id = "enter-here"
user_agent = f"linux:edu.drexel.data-science:v0.0.1 (by u/drexel_msds_stocks)"
client_secret = "enter-here"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

sub = reddit.subreddit("wallstreetbets")
for post  in sub.search("AMD", time_filter="month"):
    print(post.title)