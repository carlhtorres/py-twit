import logging, sqlite3, os
from src.logger import Logger


class Database:
    logger = Logger.logger

    try:
        os.makedirs('db')
        logging.info(Logger.message('Database', 'Created folder for database'))
    except FileExistsError:
        logging.warning('Folder for database already present')
    __database = sqlite3.connect('db/twitter.db', check_same_thread=False)
    logging.info(Logger.message('Database', 'Connection to DB open'))

    # TODO be careful, allowing multiple threads may run in concurrency issues

    @staticmethod
    def database_setup():
        Database.__table_tweet_create()
        Database.__table_hashtags_create()
        Database.__table_hashtags_fill()
        logging.info(Logger.message('Database', 'Tables created succesfully'))

    @staticmethod
    def database_close():
        Database.__database.commit()
        logging.info(Logger.message('Database', 'Committing last changes'))
        Database.__database.close()
        logging.info(Logger.message('Database', 'Database connection closed succesfully'))
        # TODO check if this may throws errors
        #  I should apply TDD if have time
        #  and convert to creator/destructor

    @staticmethod
    def __table_hashtags_create():
        try:
            Database.__database.execute('CREATE TABLE hashtags (hashtag text primary key)')
            Database.__database.commit()
            logging.info(Logger.message('Database', 'Created hashtags table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Failed to create table hashtag'))

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
            logging.info(Logger.message('Database', 'Created tweets table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Failed to create table tweets'))

    @staticmethod
    def __table_hashtags_fill():
        try:
            # TODO create API to insert hashtags
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
            logging.info(Logger.message('Database', 'Filled hashtag table with hashtags'))
        except sqlite3.IntegrityError:
            logging.warning(Logger.message('Database', 'Hashtags already present on table'))

    @staticmethod
    def hashtags():
        try:
            dataset = Database.__database.execute('SELECT hashtag FROM hashtags;').fetchall()
            logging.info(Logger.message('Database', 'Selected all hashtags from table'))
            return dataset
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Problem querying hashtags'))

    @staticmethod
    def write_tweet(tweet):
        try:
            # TODO sanitize input
            Database.__database.execute('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweet)
            logging.info(Logger.message('Database', 'Wrote tweet to table'))
            logging.debug(Logger.message('Database', f'Wrote tweet {tweet[0]} to table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Could not write tweet to database'))
        except sqlite3.IntegrityError:
            logging.warning(Logger.message('Database', 'Tweet already saved'))

    @staticmethod
    def write_tweets(tweets):
        for tweet in tweets:
            Database.write_tweet(tweet)
            # TODO tryout sqlite3.executemany()
            #  if it is more performatic or if it can tolerate failures
            #  in the data passed
        logging.info(Logger.message('Database', 'Wrote complete tweets batch to table'))

    @staticmethod
    def tweet(id):
        try:
            print(id)
            tweet = Database.__database.execute('SELECT * FROM tweets WHERE id=?', id)
            logging.info(Logger.message('Database', 'Retrieved tweet from table'))
            logging.debug(Logger.message('Database', f'Retrieved tweet {id} from table'))
            return tweet
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Invalid ID'))

    @staticmethod
    def tweets(ids):
        tweets = []
        for id in ids:
            tweets.append(Database.tweet(id))
        logging.info(Logger.message('Database', 'Finished querying tweets table'))
        # TODO check if execute many works here too
        return tweets

    @staticmethod
    def all_tweets():
        try:
            dataset = Database.__database.execute('SELECT * FROM tweets').fetchall()
            logging.info(Logger.message('Database', 'Retrieved all tweets from table'))
            return dataset
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Problem querying tweets'))
