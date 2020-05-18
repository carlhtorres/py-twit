import os, logging
from src.client import Twitter
from src.database import Database
from src.server import Server
from src.logger import Logger


def main():
    logger = Logger.logger

    twitter = Twitter()
    twitter.connect(
        os.environ.get('API_KEY'),
        os.environ.get('API_KEY_SECRET'),
        os.environ.get('ACCESS_TOKEN_KEY'),
        os.environ.get('ACCESS_TOKEN_SECRET'),
    )

    Database.database_setup()

    Server.run(host='0.0.0.0', port=8000)

    Database.database_close()
    logging.info('Finished execution')


if __name__ == '__main__':
    main()
