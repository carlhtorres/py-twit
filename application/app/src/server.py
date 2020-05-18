import json, logging, flask
from prometheus_client import Summary, make_wsgi_app
from src.database import Database
from src.logger import Logger

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

class Server:
    __app = flask.Flask(__name__)
    __app.secret_key = "makemerandom"

    # @staticmethod
    # @__app.route('/')
    # def index():
    #     return flask.render_template('index.html', title='py-Twit')
    #
    # @staticmethod
    # @__app.route('/favicon.ico')
    # def favicon():
    #     return flask.send_from_directory(flask.url_for('static'), filename='favicon.ico')

    # @staticmethod
    # @__app.route('/api/create', methods=['POST', ])
    # def create():
    #     pass

    @staticmethod
    @__app.route('/api/read/<tweet_id>')
    @REQUEST_TIME.time()
    def read(tweet_id):
        return json.dumps(Database.tweet(tweet_id))

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
        Server.__app.run(host=host, port=port)
