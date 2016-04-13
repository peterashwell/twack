import os
import time

import tweepy

from Auth import tweepy_with_auth


TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FRIENDS_IDS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FOLLOWER_IDS_API_MAX_COUNT = 5000
TWITTER_FRIENDS_IDS_API_MAX_COUNT = 5000


class MyStatus:
    def __init__(self):
        self.my_screen_name = os.environ['TWACK_MY_TWITTER_SCREEN_NAME']
        self.my_followers_path = os.environ['TWACK_MY_FOLLOWER_IDS_PATH']
        self.my_friends_path = os.environ['TWACK_MY_FRIEND_IDS_PATH']

    def get_my_followers(self):
        my_follower_ids = []

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers_ids,
            screen_name=self.my_screen_name,
            count=TWITTER_FOLLOWER_IDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            my_follower_ids.extend(page)
            time.sleep(TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS)

        return list(map(str, my_follower_ids))

    def get_my_friends(self):
        my_friend_ids = []

        cursor = tweepy.Cursor(
            tweepy_with_auth.friends_ids,
            screen_name=self.my_screen_name,
            count=TWITTER_FRIENDS_IDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            my_friend_ids.extend(page)
            time.sleep(TWITTER_FRIENDS_IDS_API_REQUEST_SPACING_SECONDS)

        return list(map(str, my_friend_ids))

    def dump_followers(self):
        follower_ids = self.get_my_followers()
        with open(self.my_followers_path, 'w') as my_followers_file:
            my_followers_file.write('\n'.join(follower_ids))

    def load_followers(self):
        with open(self.my_followers_path) as my_followers_file:
            my_follower_ids = my_followers_file.read().strip().split('\n')
        return my_follower_ids

    def dump_friends(self):
        friend_ids = self.get_my_friends()
        with open(self.my_friends_path, 'w') as my_friends_file:
            my_friends_file.write('\n'.join(friend_ids))

    def load_friends(self):
        with open(self.my_friends_path) as my_friends_file:
            my_friend_ids = my_friends_file.read().strip().split('\n')
        return my_friend_ids

    def load_follow_backs(self):
        my_follower_ids = status.load_followers()
        my_friend_ids = status.load_friends()
        follow_backs = set(my_follower_ids).intersection(my_friend_ids)

        return follow_backs

if __name__ == '__main__':
    status = MyStatus()
    my_follower_ids = status.load_followers()
    my_friend_ids = status.load_friends()
    follow_backs = status.load_follow_backs()

    print('{0} friends, {1} followers, {2} follow-backs'.format(
        len(my_friend_ids), len(my_follower_ids), len(follow_backs)
    ))
