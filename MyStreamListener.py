import json
import tweepy
import tweepy as tw
from config import create_api

# Authenticate to Twitter
api = create_api()


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")


tweets = api.mentions_timeline()
for tweet in tweets:
    tweet.favorite()
    tweet.user.follow()

# Create API object
api = create_api()
tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.filter(track=["Python", "Django", "Tweepy"], languages=["en"])
for tweet in tweepy.Cursor(api.home_timeline).items(100):
    print(f"{tweet.user.name} said: {tweet.text}")
