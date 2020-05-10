import sqlite3


class Database:
    __main = sqlite3.connect('db/main.db', check_same_thread=False)
    __aux = sqlite3.connect('db/aux.db', check_same_thread=False)
    # TODO be careful, allowing multiple threads may run in concurrency issues

    @classmethod
    def close_database(cls):
        Database.__aux.close()
        Database.__main.close()

    @staticmethod
    def setup():
        try:
            Database.__create_aux_tables()
            Database.__create_table_tweet()
        except sqlite3.OperationalError:
            print('Fucked up the db')

    @staticmethod
    def __create_aux_tables():
        try:
            Database.__aux.execute('CREATE TABLE hashtags (hashtag text primary key)')
        except sqlite3.OperationalError:
            # TODO improve and add log
            print("DATABASE ALREADY EXISTS!")

    @classmethod
    def __create_table_tweet(cls):
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

    @staticmethod
    def __fill_aux_table():
        try:
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
    def hashtags(cls):
        try:
            Database.__fill_aux_table()
        except sqlite3.OperationalError:
            # TODO treat this error
            print("FIX ME! Database.hashtags")

        return Database.__aux.execute('''SELECT hashtag FROM hashtags;''').fetchall()


    @classmethod
    def write_tweet(cls, tweet):
        try:
            Database.__main.execute('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweet)
        except sqlite3.OperationalError:
            # TODO yeah
            print("Can't write tweet")

    @classmethod
    def write_tweets(cls, tweets):
        for tweet in tweets:
            # TODO sanitize data
            Database.write_tweet(tweet)
            # TODO tryout sqlite3.executemany()
            # if it is more performatic or if it can tolerate failures
            # in the data passed

    @classmethod
    def tweet(cls, id):
        try:
            Database.__main.execute('SELECT * FROM tweets WHERE id=?', id)
        except sqlite3.OperationalError:
            print('Invalid ID')
            return None

    @classmethod
    def tweets(cls, ids):
        tweets = []
        for id in ids:
            tweets.append(Database.tweet(id))
        # TODO check if execute many works here too
        return tweets

    @classmethod
    def all_tweets(cls):
        return Database.__main.execute('SELECT * FROM tweets')
