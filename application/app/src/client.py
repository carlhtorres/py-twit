from twitter.api import Api, TwitterError


class Twitter:
    __api_key = "__api key"
    __api_key_secret = "__api key secret"
    __access_token_key = "access token key"
    __access_token_secret = "access token secret"
    __api = Api

    @staticmethod
    def __credentials(api_key, api_key_secret, access_token_key, access_token_secret):
        # TODO change behaviour to import from ENV VARS
        #  if they are not passed as arguments
        Twitter.__api_key = api_key
        Twitter.__api_key_secret = api_key_secret
        Twitter.__access_token_key = access_token_key
        Twitter.__access_token_secret = access_token_secret

    @staticmethod
    def connect(api_key, api_key_secret, access_token_key, access_token_secret):
        Twitter.__credentials(api_key, api_key_secret, access_token_key, access_token_secret)
        try:
            Twitter.__api = Api(
                consumer_key=api_key,
                consumer_secret=api_key_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
        except TwitterError:
            print("FIX ME! Twitter.connect")

    @staticmethod
    def search(query):
        try:
            return Twitter.__api.GetSearch(raw_query=query, return_json=True)
            # TODO handle timeouts and limits
        except TwitterError:
            print("FIX ME! Twitter.search")
