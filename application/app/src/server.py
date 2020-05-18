import json, logging, flask
from prometheus_client import Summary, make_wsgi_app
from src.database import Database
from src.logger import Logger
from src.client import Twitter

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


class Server:
    __app = flask.Flask(__name__, static_url_path='', static_folder='static')
    __app.secret_key = "makemerandom"

    # @staticmethod
    # @__app.route('/')
    # def index():
    #     return flask.render_template('index.html', title='py-Twit')

    @staticmethod
    @__app.route('/favicon.ico')
    def favicon():
        return Server.__app.send_static_file('favicon.ico')

    # @staticmethod
    # @__app.route('/api/create', methods=['POST', ])
    # def create():
    #     pass

    @staticmethod
    @__app.route('/api/read/tweet/<tweet_id>')
    @REQUEST_TIME.time()
    def read_tweet(tweet_id):
        try:
            raw = Database.get_tweet(tweet_id)
            return json.dumps(raw)
        except ValueError:
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @staticmethod
    @__app.route('/api/read/hashtag/<hashtag>')
    @REQUEST_TIME.time()
    def read_hashtag(hashtag):
        try:
            return json.dumps(Database.get_tweet_list(hashtag))
        except ValueError:
            return json.dumps({'success': False}), 500, {'ContentType': 'application/json'}

    @staticmethod
    @__app.route('/api/search/all')
    @REQUEST_TIME.time()
    def search_all():
        twitter = Twitter()
        for hashtag in Database.hashtags():
            # TODO stop using index on  hashtag
            for tweet in twitter.search(f'q=%23{hashtag[0]}')["statuses"]:
                Database.write_data(tweet)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    @staticmethod
    @__app.route('/api/statistics/users')
    @REQUEST_TIME.time()
    def statistics_users():
        return json.dumps(Database.get_user_top_followers())

    @staticmethod
    @__app.route('/api/statistics/tweets')
    @REQUEST_TIME.time()
    def statistics_tweets():
        statistics = Database.get_tweets_by_hour()
        data = []
        for entry in statistics:
            dict = {
                'time': entry[0],
            }
            data.append(dict)
        return json.dumps(data)

    # @staticmethod
    # @__app.route('/api/update', methods=['PUT', ])
    # def update():
    #     pass
    #
    # @staticmethod
    # @__app.route('/api/delete')
    # def delete():
    #     pass

    @staticmethod
    @__app.route('/metrics')
    def metrics():
        logging.info(Logger.message('Server', 'Scrapping prometheus metrics'))
        return make_wsgi_app()

    @staticmethod
    def run(host, port):
        logging.info(Logger.message('Server', 'Starting flask server'))
        Server.__app.run(host=host, port=port, debug=True)
