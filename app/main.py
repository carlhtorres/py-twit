import json
import os
import sys

from flask import Flask, render_template, send_from_directory, request

from app.src.client import Twitter
from app.src.database import Database

app = Flask(__name__)
twitter = Twitter()
# TODO add credentials from ENV VARS
twitter.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# TODO new class to integrate DB and twitter api?
tweets = []
for hashtag in Database.hashtags():
    # TODO do I need this index?
    for tweet in twitter.search(f'q=%23{hashtag[0]}')["statuses"]:
        tweets.append(tweet)


@app.route('/tweets')
def tweets():
    return json.dumps(tweets)


@app.route('/')
def index():
    return render_template('index.html', titulo='py-Twit')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


@app.route('/put-something', methods=['POST', ])
def put_rest():
    something = request.form['filter']
    # PUT command


app.run(host='0.0.0.0', port=8000)
