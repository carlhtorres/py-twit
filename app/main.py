import flask, json, sys

from app.src.client import Twitter
from app.src.database import Database

app = flask.Flask(__name__)
twitter = Twitter()
# TODO add credentials from ENV VARS
twitter.connect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# TODO new class to integrate DB and twitter api?
tweets = []
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
        tweets.append(fmt_tweet)


@app.route('/tweets')
def tweets():
    return json.dumps(tweets)


@app.route('/')
def index():
    return flask.render_template('index.html', title='py-Twit')


# @app.route('/favicon.ico')
# def favicon():
#     return flask.send_from_directory(flask.url_for('static'), filename='favicon.ico')


# @app.route('/put-something', methods=['POST', ])
# def put_rest():
#     something = flask.request.form['filter']
#     # PUT command
#     return flask.redirect('/')


app.run(host='0.0.0.0', port=8000)
