import os
import time

import tweepy

from Auth import tweepy_with_auth


TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FOLLOWER_IDS_API_MAX_COUNT = 5000


class MyStatus:
    def __init__(self):
        self.screen_name = os.environ['TWACK_MY_TWITTER_SCREEN_NAME']
        self.my_followers_path = os.environ['TWACK_MY_FOLLOWER_IDS_PATH']

    def get_my_followers(self):
        my_follower_ids = []

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers_ids,
            screen_name=self.screen_name,
            count=TWITTER_FOLLOWER_IDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            my_follower_ids.extend(page)
            time.sleep(TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS)

        return list(map(str, my_follower_ids))

    def dump_followers(self):
        follower_ids = self.get_my_followers()
        with open(self.my_followers_path, 'w') as my_followers_file:
            my_followers_file.write('\n'.join(follower_ids))

    def load_followers(self):
        with open(self.my_followers_path) as my_followers_file:
            my_follower_ids = my_followers_file.read().strip().split('\n')
        return my_follower_ids

if __name__ == '__main__':
    status = MyStatus()
    followers = status.get_my_followers()
    status.dump_followers()
