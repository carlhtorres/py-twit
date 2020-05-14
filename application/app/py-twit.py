import sys, os, logging
import prometheus_client
from src.client import Twitter
from src.database import Database
from src.server import Server
from src.logger import Logger

REQUEST_TIME =

def main():
    logger = Logger.logger
    twitter = Twitter()
    # TODO add credentials from ENV VARS
    twitter.connect(
        os.environ.get('API_KEY'),
        os.environ.get('API_KEY_SECRET'),
        os.environ.get('ACCESS_TOKEN_KEY'),
        os.environ.get('ACCESS_TOKEN_SECRET'),
    )
    Database.database_setup()

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

    Server.run(host='0.0.0.0', port=8000)

    Database.database_close()

    logging.info('Finished execution')


if __name__ == '__main__':
    main()
