import os

import tweepy

access_token = os.environ['TWACK_TWITTER_API_ACCESS_TOKEN']
access_token_secret = os.environ['TWACK_TWITTER_API_ACCESS_TOKEN_SECRET']

consumer_key = os.environ['TWACK_TWITTER_API_CONSUMER_KEY']
consumer_secret = os.environ['TWACK_TWITTER_API_CONSUMER_SECRET']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepy_with_auth = tweepy.API(auth)


class TwitterConstants:
    FOLLOWERS_API_SLEEP_SECONDS = 60
    FRIENDS_API_SLEEP_SECONDS = 60

    FRIENDS_API_MAX_COUNT = 200
    FOLLOWERS_API_MAX_COUNT = 200
    FAVORITES_API_MAX_COUNT = 200

    CREATE_FRIENDSHIP_API_SLEEP_SECONDS = 1200 # 20 minutes
    CREATE_FAVORITE_API_SLEEP_SECONDS = 2400 # 40 minutes
