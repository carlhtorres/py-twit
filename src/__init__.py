import time
import twitter
import sys
import sqlite3

api_key = sys.argv[1]
api_key_secret = sys.argv[2]
access_token_key = sys.argv[3]
access_token_secret = sys.argv[4]

api = twitter.Api(consumer_key=api_key, consumer_secret=api_key_secret, access_token_key=access_token_key,
                  access_token_secret=access_token_secret)

results = api.GetSearch(raw_query="q=%23devops", return_json=True)

conn = sqlite3.connect('../db/main.db')

c = conn.cursor()

try:
    c.execute("CREATE TABLE tweets (json text, date date)")
except sqlite3.OperationalError:
    pass

insert_db = []
for result in results:
    insert_db.append(tuple((str(result), time.time())))

c.executemany('INSERT INTO tweets VALUES(?,?)', insert_db)

conn.commit()

conn.close()


