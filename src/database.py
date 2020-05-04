import sqlite3


# TODO logs here
class Database:
    __main = sqlite3.connect('db/main.db')
    __aux = sqlite3.connect('db/aux.db')

    @classmethod
    def close_database(cls):
        Database.__aux.close()
        Database.__main.close()

    @classmethod
    def write_tweet(cls, tweet):
        Database.__main.execute('')

    @classmethod
    def hashtags(cls):
        try:
            query = 'SELECT hashtags FROM hashtag'
            return Database.__aux.execute(query)
        except TypeError:
            print("FIX ME!")
            # TODO obvious

    @classmethod
    def __create_table_tweet(cls):
        create = "CREATE TABLE tweets (json text, date date)"
        try:
            Database.__main.execute(create)
        except sqlite3.OperationalError:
            raise sqlite3.OperationalError('Could not create database!')

    @classmethod
    def write_tweet(cls, tweet):
        # TODO implement
        pass

    @classmethod
    def write_tweets(cls, tweets):
        for tweet in tweets:
            # TODO sanitize data
            Database.write_tweet(tweet)

    @classmethod
    def tweet(cls, id):
        pass

    @classmethod
    def tweets(cls, ids):
        pass

    @classmethod
    def all_tweets(cls, page):
        pass
