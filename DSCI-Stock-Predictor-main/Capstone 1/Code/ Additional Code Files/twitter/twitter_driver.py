import time

from file_service import FileService
from search_service import SearchService
from calendar import monthrange


def get_dates(year:int, month:int, append=False):
    m = ['{:04d}-{:02d}-{:02d}'.format(year, month, d)
            for d in range(1, monthrange(year, month)[1] + 1)]
    if append:
        m_plus_1 = (month+1)%12
        m_plus_1 = ['{:04d}-{:02d}-{:02d}'.format(year, m_plus_1, d)
            for d in range(1, monthrange(year, m_plus_1)[1] + 1)]
        m.append(m_plus_1[0])
    return m


def main():
    fs = FileService()
    twitter = SearchService()

    ticker = "TSLA"

    # Get Tweets from 01/01/2021 through 04/30/2021
    dates = get_dates(2021, 1)
    dates.extend(get_dates(2021, 2))
    dates.extend(get_dates(2021, 3))
    dates.extend(get_dates(2021, 4, True))

    file_path = f"tweets/{ticker}"
    for r in range(len(dates)-1):
        start = dates[r]
        end = dates[r + 1]

        if fs.file_exists(f"{file_path}/{start}.json"):
            print(f"Skipping Posts: {start}-{end}")
            continue

        print(f"Acquiring Tweets: {start}-{end}")
        tweets = twitter.search(ticker, start, end, max_results=2000)

        fs.save_file(tweets, f"{file_path}/{start}.json")
        time.sleep(3)

if __name__ == '__main__':
    main()