import flask

from database import Database


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
    @__app.route('/api/read')
    def read():
        print('Returning all tweets saved!\nFix this fuckery shit!\nAnd make it jsons, for Odins sake')
        return Database.tweets()

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
    def run(host, port):
        Server.__app.run(host=host, port=port)
