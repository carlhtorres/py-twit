import logging
from twitter.api import Api, TwitterError
from src.logger import Logger


class Twitter:
    logger = Logger.logger
    __api = Api

    @staticmethod
    def connect(api_key, api_key_secret, access_token_key, access_token_secret):
        try:
            Twitter.__api = Api(
                consumer_key=api_key,
                consumer_secret=api_key_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
            logging.info(Logger.message('Twitter', 'Connection stablished'))
        except TwitterError:
            logging.error(Logger.message('Twitter', 'Could not stablish a connection to Twitter API'))

    @staticmethod
    def search(query):
        try:
            logging.info(Logger.message('Twitter', f'Searching for {query}'))
            return Twitter.__api.GetSearch(raw_query=query, return_json=True)
            # TODO handle timeouts and limits
        except TwitterError:
            logging.error(Logger.message('Twitter', 'Search failed'))
