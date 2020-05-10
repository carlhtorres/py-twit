import flask, json, sys

from app.src.client import Twitter
from app.src.database import Database
from app.src.server import Server


twitter = Twitter()
# TODO add credentials from ENV VARS
twitter.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# TODO new class to integrate DB and twitter api?
for hashtag in Database.hashtags():
    # TODO stop using index on  hashtag
    for tweet in twitter.search(f'q=%23{hashtag[0]}')["statuses"]:
        # TODO why can't I cast directly to a n-tuple?
        fmt_tweet = (
            tweet['id'],
            tweet['created_at'],
            str(tweet['text']),
            # TODO text concatenated
            hashtag[0],
            tweet['user']['screen_name'])
        Database.write_tweet(fmt_tweet)

# Server.run(host='0.0.0.0', port=8000)
