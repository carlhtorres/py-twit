import twitter


class Twitter():
    api_key = "api key"
    api_key_secret = "api key secret"
    access_token_key = "access token key"
    access_token_secret = "access token secret"
    api = twitter.Api


    @staticmethod
    def search(query):
        try:
            return Twitter.api.GetSearch(raw_query=query, return_json=True)
        except twitter.TwitterError:
            print("FIX ME!")

    @staticmethod
    def __credentials(api_key, api_key_secret, access_token_key, access_token_secret):
        Twitter.api_key = api_key
        Twitter.api_key_secret = api_key_secret
        Twitter.access_token_key = access_token_key
        Twitter.access_token_secret = access_token_secret

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
            print("FIX ME!")
