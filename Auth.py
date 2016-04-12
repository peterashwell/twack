import os

import tweepy

access_token = os.environ['TWACK_TWITTER_API_ACCESS_TOKEN']
access_token_secret = os.environ['TWACK_TWITTER_API_ACCESS_TOKEN_SECRET']

consumer_key = os.environ['TWACK_TWITTER_API_CONSUMER_KEY']
consumer_secret = os.environ['TWACK_TWITTER_API_CONSUMER_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepy_with_auth = tweepy.API(auth)
