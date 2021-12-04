import requests
from retry import retry
import tweepy

# -------------------------------
# Twitternotify Class
# -------------------------------
class Twitternotify:

    def __init__(self, twitter_api_key, twitter_api_secret, twitter_token, twitter_token_secret, exchange):
        self.auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
        self.auth.set_access_token(twitter_token, twitter_token_secret)
        self.api = tweepy.API(self.auth)
        self.exchange = exchange

    @retry(requests.exceptions.ConnectionError, tries=100, delay=1)
    def send(self, *lines):
        message = ''
        for obj in lines:
            message += '\n' + obj
        payload = '{}\n\n#MacaronDream #仮想通貨 #自動売買 #BTCFX #Cryptocurrency #{}'.format(message, self.exchange)
        #files = '/tmp/' + self.tv_dir + '.png'
        #files = r'c:\tmp\sceeenshot1.png'
        #self.api.update_status_with_media(status=payload, filename=files)
        self.api.update_status(payload)

# -------------------------------
# EOF
# -------------------------------