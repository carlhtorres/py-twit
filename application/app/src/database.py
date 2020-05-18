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
        Database.__table_user_create()
        Database.__table_hashtags_create()
        Database.__table_hashtags_fill()
        Database.__database.commit()
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

    @staticmethod
    def __table_tweet_create():
        create = '''CREATE TABLE tweets (
                        id text primary key,
                        created_at date,
                        text text,
                        hashtag text,
                        user_id text
                    )'''
        try:
            Database.__database.execute(create)
            Database.__database.commit()
            logging.info(Logger.message('Database', 'Created tweets table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Failed to create table tweets'))

    @staticmethod
    def __table_user_create():
        create = '''CREATE TABLE users (
                        id text primary key,
                        screen_name text,
                        name text,
                        location text,
                        lang text
                    )'''
        try:
            Database.__database.execute(create)
            Database.__database.commit()
            logging.info(Logger.message('Database', 'Created users table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Failed to create table users'))

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
    def __tweet_format_tuple(tweet):
        return (
            tweet['id'],
            tweet['created_at'],
            str(tweet['full_text']),
            Database.__tweet_hashtags(tweet['entities']['hashtags']),
            tweet['user']['id'],
        )

    @staticmethod
    def __tweet_hashtags(json):
        hashtags = []
        for hashtag in json:
            hashtags.append(hashtag['text'])
        return str(hashtags)

    @staticmethod
    def __tweet_tuple_to_dict(tweet):
        return {
            "id"      : tweet[0],
            "date"    : tweet[1],
            "message" : tweet[2],
            "hashtags": tweet[3],
            "user_id" : tweet[4]
        }

    @staticmethod
    def __user_format_tuple(tweet):
        user_json = tweet['user']
        return (
            user_json['id'],
            user_json['screen_name'],
            user_json['name'],
            user_json['location'],
            tweet['lang']
        )

    @staticmethod
    def __user_tuple_to_dict(user):
        return {
            "id"         : user[0],
            "screen_name": user[1],
            "name"       : user[2],
            "location"   : user[3],
            "lang"       : user[4]
        }

    @staticmethod
    def hashtags():
        try:
            dataset = Database.__database.execute('SELECT hashtag FROM hashtags;').fetchall()
            logging.info(Logger.message('Database', 'Selected all hashtags from table'))
            return dataset
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Problem querying hashtags'))

    @staticmethod
    def __write_tweet(tweet):
        try:
            # TODO sanitize input
            Database.__database.execute(
                'INSERT INTO tweets VALUES (?, ?, ?, ?, ?)',
                Database.__tweet_format_tuple(tweet)
            )
            Database.__database.commit()
            logging.debug(Logger.message('Database', f'Wrote tweet to table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Could not write tweet to table'))
        except sqlite3.IntegrityError:
            logging.warning(Logger.message('Database', 'Tweet already saved'))

    @staticmethod
    def __write_user(tweet):
        try:
            Database.__database.execute(
                'INSERT INTO users VALUES (?, ?, ?, ?, ?)',
                Database.__user_format_tuple(tweet)
            )
            Database.__database.commit()
            logging.debug(Logger.message('Database', f'Wrote user to table'))
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Could not write user to table'))
        except sqlite3.IntegrityError:
            logging.warning(Logger.message('Database', 'User already saved'))

    @staticmethod
    def write_data(tweet):
        try:
            Database.__write_tweet(tweet)
            Database.__write_user(tweet)
        except TypeError:
            logging.warning(Logger.message('Database', 'Could not save data'))

    @staticmethod
    def write_tweets(tweets):
        for tweet in tweets:
            Database.write_data(tweet)
        logging.info(Logger.message('Database', 'Wrote complete tweets batch to table'))

    @staticmethod
    def tweet(id):
        try:
            tweet = Database.__database.execute(f'SELECT * FROM tweets WHERE id={id}').fetchone()
            if tweet is not None:
                logging.debug(Logger.message('Database', f'Retrieved tweet {id} from table'))
                return Database.__tweet_tuple_to_dict(tweet)
            raise ValueError('Invalid ID')
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Operational error'))
        except sqlite3.ProgrammingError:
            logging.warning(Logger.message('Database', 'Invalid query'))

    @staticmethod
    def tweets(ids):
        tweets = []
        for id in ids:
            tweets.append(Database.tweet(id))
        logging.info(Logger.message('Database', 'Finished querying tweets table'))
        return tweets

    @staticmethod
    def all_tweets():
        try:
            dataset = Database.__database.execute('SELECT * FROM tweets').fetchall()
            fmt_tweets = []
            for tweet in dataset:
                fmt_tweets.append(Database.__tweet_tuple_to_dict(tweet))
            logging.info(Logger.message('Database', 'Retrieved all tweets from table'))
            return fmt_tweets
        except sqlite3.OperationalError:
            logging.warning(Logger.message('Database', 'Problem querying tweets'))
