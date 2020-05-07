import sqlite3


class Database:
    __main = sqlite3.connect('db/main.db', check_same_thread=False)
    __aux = sqlite3.connect('db/aux.db', check_same_thread=False)
    # TODO be careful, allowing multiple threads may run in concurrency issues

    @staticmethod
    def __create_aux_tables():
        try:
            Database.__aux.execute('''CREATE TABLE hashtags (hashtag text primary key);''')
        except sqlite3.OperationalError:
            # TODO improve and add log
            print("DATABASE ALREADY EXISTS!")


    @staticmethod
    def __fill_aux_table():
        try:
            Database.__create_aux_tables()
            # TODO improve inserting/importing this data
            Database.__aux.execute('''INSERT INTO hashtags
            VALUES
            ('openbanking'),
            ('remediation'),
            ('devops'),
            ('sre'),
            ('microservices'),
            ('observability'),
            ('oauth'),
            ('metrics'),
            ('logmonitoring'),
            ('opentracing');
            ''')
            Database.__aux.commit()
        except sqlite3.IntegrityError:
            # TODO ...
            print("HASHTAGS ALREADY CREATED!")

    @classmethod
    def close_database(cls):
        Database.__aux.close()
        Database.__main.close()

    @classmethod
    def hashtags(cls):
        try:
            Database.__fill_aux_table()
        except sqlite3.OperationalError:
            # TODO treat this error
            print("FIX ME! Database.hashtags")

        return Database.__aux.execute('''SELECT hashtag FROM hashtags;''').fetchall()

    @classmethod
    def create_table_tweet(cls):
        create = '''CREATE TABLE tweets (
                    id text primary key,
                    created_at date,
                    text text,
                    hashtag text,
                    user text);'''
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