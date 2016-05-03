import json
import os
import time

import tweepy

from TwitterApi import (
    tweepy_with_auth,
    tweepy_user_to_twack_user,
    TwitterConstants
)
from Meta import seed_screen_names
from TwackData import TwackTwitterUser, TwackData


class MyStatus:
    def __init__(self):
        self.my_screen_name = os.environ['TWACK_MY_TWITTER_SCREEN_NAME']
        self.my_followers_path = os.environ['TWACK_MY_FOLLOWER_IDS_PATH']
        self.my_friends_path = os.environ['TWACK_MY_FRIEND_IDS_PATH']

        self.twack_data = TwackData()

    def dump_seed_followers(self):
        for seed_screen_name in seed_screen_names:
            cursor = tweepy.Cursor(
                tweepy_with_auth.followers,
                screen_name=seed_screen_name,
                count=TwitterConstants.TWITTER_FOLLOWERS_API_MAX_COUNT
            )

            for page in cursor.pages():
                for user in page:
                    twack_twitter_user = tweepy_user_to_twack_user(user)
                    self.twack_data.add_twack_twitter_user(twack_twitter_user)
                    self.twack_data.add_follower_of_screen_name(
                        twack_twitter_user, seed_screen_name
                    )
                time.sleep(
                    TwitterConstants.TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS
                )

    def dump_my_followers(self):
        self.twack_data.delete_all_my_followers()

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers,
            screen_name=self.my_screen_name,
            count=TwitterConstants.TWITTER_FOLLOWERS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user in page:
                twack_twitter_user = tweepy_user_to_twack_user(user)
                self.twack_data.add_twack_twitter_user(twack_twitter_user)
                self.twack_data.add_my_follower(twack_twitter_user)
            time.sleep(
                TwitterConstants.TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS
            )

    def dump_my_friends(self):
        self.twack_data.delete_all_my_friends()

        cursor = tweepy.Cursor(
            tweepy_with_auth.friends,
            screen_name=self.my_screen_name,
            count=TwitterConstants.TWITTER_FRIENDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user in page:
                twack_twitter_user = tweepy_user_to_twack_user(user)
                self.twack_data.add_twack_twitter_user(twack_twitter_user)
                self.twack_data.add_my_friend(twack_twitter_user)
            time.sleep(TwitterConstants.TWITTER_FRIENDS_API_REQUEST_SPACING_SECONDS)

    def find_unfriendly_friends(self):
        my_followers = self.twack_data.load_my_followers()
        my_friends = self.twack_data.load_my_friends()

        my_followers_ids = {f.user_id for f in my_followers}
        my_friends_ids = {f.user_id for f in my_friends}

        unfriendly = my_friends_ids.difference(my_followers_ids)
        return unfriendly

if __name__ == '__main__':
    status = MyStatus()
    tw = TwackData()

    my_followers = tw.load_my_followers()
    my_friends = tw.load_my_friends()
    unfriendly = status.find_unfriendly_friends()

    print('{0} friends, {1} followers, {2} unfriendlies'.format(
        len(my_friends), len(my_followers), len(unfriendly)
    ))
