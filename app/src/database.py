import sqlite3


class Database:
    __database = sqlite3.connect('db/twitter.db', check_same_thread=False)
    # TODO be careful, allowing multiple threads may run in concurrency issues

    @staticmethod
    def database_setup():
        Database.__table_tweet_create()
        Database.__table_hashtags_create()
        Database.__table_hashtags_fill()
        print("All set and ready to go!")

    @classmethod
    def database_close(cls):
        Database.__database.commit()
        print("Committing last changes")
        Database.__database.close()
        print("Bye!")
        # TODO check if this may throws errors
        #  I should apply TDD if have time
        #  and convert to creator/destructor

    @staticmethod
    def __table_hashtags_create():
        try:
            Database.__database.execute('CREATE TABLE hashtags (hashtag text primary key)')
            Database.__database.commit()
        except sqlite3.OperationalError:
            print("Could not create table")

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
        except sqlite3.OperationalError:
            print("Could not create table")

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
        except sqlite3.IntegrityError:
            print("HASHTAGS ALREADY CREATED!")

    @classmethod
    def hashtags(cls):
        try:
            return Database.__database.execute('SELECT hashtag FROM hashtags;').fetchall()
        except sqlite3.OperationalError:
            print("Shit went bad")

    @classmethod
    def write_tweet(cls, tweet):
        try:
            # TODO sanitize input
            Database.__database.execute('INSERT INTO tweets VALUES (?, ?, ?, ?, ?)', tweet)
        except sqlite3.OperationalError:
            # TODO yeah
            print("Can't write tweet")
        except sqlite3.IntegrityError:
            print("Tweet already saved!")

    @classmethod
    def write_tweets(cls, tweets):
        for tweet in tweets:
            Database.write_tweet(tweet)
            # TODO tryout sqlite3.executemany()
            #  if it is more performatic or if it can tolerate failures
            #  in the data passed

    @staticmethod
    def tweet(id):
        try:
            Database.__database.execute('SELECT * FROM tweets WHERE id=?', id)
        except sqlite3.OperationalError:
            print('Invalid ID')

    @staticmethod
    def tweets(ids):
        tweets = []
        for id in ids:
            tweets.append(Database.tweet(id))
        # TODO check if execute many works here too
        return tweets

    @staticmethod
    def all_tweets():
        # TODO try catch...
        return Database.__database.execute('SELECT * FROM tweets').fetchall()
