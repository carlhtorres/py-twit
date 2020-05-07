import twitter


class Twitter:
    __api_key = "api key"
    __api_key_secret = "api key secret"
    __access_token_key = "access token key"
    __access_token_secret = "access token secret"
    # TODO make this private WITHOUT breaking the rest
    api = twitter.Api

    @staticmethod
    def search(query):
        try:
            return Twitter.api.GetSearch(raw_query=query, return_json=True)
        except twitter.TwitterError:
            # TODO log errors
            print("FIX ME! Twitter.search")

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
            Twitter.api = twitter.Api(
                consumer_key=api_key,
                consumer_secret=api_key_secret,
                access_token_key=access_token_key,
                access_token_secret=access_token_secret
            )
        except twitter.TwitterError:
            # TODO log everytime this is called
            print("FIX ME! Twitter.connect")