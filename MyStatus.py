import os

import tweepy

from Auth import tweepy_with_auth


TWITTER_FOLLOWERS_BY_ID_API_REQUEST_SPACING_SECONDS = 60


class MyStatus:
    def __init__(self):
        self.screen_name = os.environ['TWACK_MY_TWITTER_SCREEN_NAME']
        self.my_followers_path = os.environ['TWACK_MY_FOLLOWER_IDS_PATH']

    def get_my_followers(self):
        my_follower_ids = []

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers_ids, self.screen_name
        )
        for page in cursor.pages():
            my_follower_ids.extend(page)

