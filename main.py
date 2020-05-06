import sys

from src.client import Twitter
from src.database import Database

twitter = Twitter()
# TODO add credentials from ENV VARS
twitter.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

for hashtag in Database.hashtags():
    # TODO do I need this index?
    tweets = twitter.search(f'q=%23{hashtag[0]}')
    print(hashtag[0], len(tweets["statuses"]), tweets["statuses"])
