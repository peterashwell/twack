import os
import sqlite3

from collections import namedtuple

TwackTwitterUser = namedtuple(
    'TwackTwitterUser',
    'id, user_id, screen_name, followers_count, friends_count, blob'
)


class TwackData:
    def __init__(self):
        self.db = sqlite3.connect(os.environ['TWACK_DB_PATH'])

    def add_user(self, twack_twitter_user):
        pass

    def add_follow_attempt(self, twack_twitter_user):
        pass

    def add_seed_follower(self, twack_twitter_user, follower_of_screen_name):
        pass

    def add_my_follower(self, twack_twitter_user):
        pass

    def clear_all_followers(self):
        pass

    def add_my_friend(self, twack_twitter_user):
        pass

    def clear_all_friends(self):
        pass
