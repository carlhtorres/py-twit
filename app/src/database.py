import logging
import sqlite3


class Database:
    __database = sqlite3.connect('db/twitter.db', check_same_thread=False)
    logging.info('Connection to DB open')
    # TODO be careful, allowing multiple threads may run in concurrency issues

    @staticmethod
    def database_setup():
        Database.__table_tweet_create()
        Database.__table_hashtags_create()
        Database.__table_hashtags_fill()
        logging.info('Tables created succesfully')

    @staticmethod
    def database_close():
        Database.__database.commit()
        logging.info('Committing last changes')
        Database.__database.close()
        logging.info('Database connection closed succesfully')
        # TODO check if this may throws errors
        #  I should apply TDD if have time
        #  and convert to creator/destructor

    @staticmethod
    def __table_hashtags_create():
        try:
            Database.__database.execute('CREATE TABLE hashtags (hashtag text primary key)')
            Database.__database.commit()
            logging.info('Created hashtags table')
        except sqlite3.OperationalError:
            logging.warning('Failed to create table hashtag')

    @classmethod
    def __table_tweet_create(cls):
        create = '''CREATE TABLE tweets (
                        id text primary key,
                        created_at date,
                        text text,
                        hashtag text,
                        user text
                    )'''
        try:
            Database.__database.execute(create)
            Database.__database.commit()
            logging.info('Created tweets table')
        except sqlite3.OperationalError:
            logging.warning('Failed to create table tweets')

    @staticmethod
    def __table_hashtags_fill():
        try:
            # TODO improve inserting/importing this data
            Database.__database.execute('''
                INSERT INTO hashtags
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
                    ('opentracing')
            ''')
            Database.__database.commit()
            logging.info('Filled hashtag table with hashtags')
        except sqlite3.IntegrityError:
            logging.warning('Hashtags already present on table')

    @staticmethod
    def hashtags():
        try:
            dataset = Database.__database.execute('SELECT hashtag FROM hashtags;').fetchall()
            logging.info('Selected all hashtags from table')
            return dataset
        except sqlite3.OperationalError:
            logging.warning('Problem querying hashtags')

    @staticmethod
    def write_tweet(tweet):
        try:
            # TODO sanitize input
            Database.__database.execute('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweet)
            logging.info('Wrote tweet to table')
            logging.debug(f'Wrote tweet {tweet[0]} to table')
        except sqlite3.OperationalError:
            logging.warning('Could not write tweet to database')
        except sqlite3.IntegrityError:
            logging.warning('Tweet already saved')

    @staticmethod
    def write_tweets(tweets):
        for tweet in tweets:
            Database.write_tweet(tweet)
            # TODO tryout sqlite3.executemany()
            #  if it is more performatic or if it can tolerate failures
            #  in the data passed
        logging.info('Wrote complete tweets batch to table')

    @staticmethod
    def tweet(id):
        try:
            tweet = Database.__database.execute('SELECT * FROM tweets WHERE id=?', id)
            logging.info('Retrieved tweet from table')
            logging.debug(f'Retrieved tweet {id} from table')
            return tweet
        except sqlite3.OperationalError:
            logging.warning('Invalid ID')

    @staticmethod
    def tweets(ids):
        tweets = []
        for id in ids:
            tweets.append(Database.tweet(id))
        logging.info('Finished querying tweets table')
        # TODO check if execute many works here too
        return tweets

    @staticmethod
    def all_tweets():
        try:
            dataset = Database.__database.execute('SELECT * FROM tweets').fetchall()
            logging.info('Retrieved all tweets from table')
            return dataset
        except sqlite3.OperationalError:
            logging.warning('Problem querying tweets')
