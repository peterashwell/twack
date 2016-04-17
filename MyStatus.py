import os
import time

import tweepy

from Auth import tweepy_with_auth
from Meta import seed_screen_names
from TwackData import TwackTwitterUser, TwackData

TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FRIENDS_IDS_API_REQUEST_SPACING_SECONDS = 60

TWITTER_FOLLOWER_IDS_API_MAX_COUNT = 5000
TWITTER_FRIENDS_IDS_API_MAX_COUNT = 5000
TWITTER_FOLLOWERS_API_MAX_COUNT = 200


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
                count=TWITTER_FOLLOWERS_API_MAX_COUNT
            )

            for page in cursor.pages()[:1]:
                for user in page:
                    twack_twitter_user = TwackTwitterUser(
                        user.id_str,
                        user.screen_name,
                        user.followers_count,
                        user.friends_count,
                        user._json
                    )
                    self.twack_data.add_twack_twitter_user(twack_twitter_user)
                    self.twack_data.add_follower_of_screen_name(
                        user.id_str, seed_screen_name
                    )
                time.sleep(TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS)

    def dump_my_followers(self):
        self.twack_data.delete_all_my_followers()

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers_ids,
            screen_name=self.my_screen_name,
            count=TWITTER_FOLLOWER_IDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user_id in my_follower_ids:
                self.twack_data.add_my_follower_with_user_id(user_id)
            time.sleep(TWITTER_FOLLOWER_IDS_API_REQUEST_SPACING_SECONDS)

    def dump_my_friends(self):
        self.twack_data.delete_all_my_friends()

        cursor = tweepy.Cursor(
            tweepy_with_auth.friends_ids,
            screen_name=self.my_screen_name,
            count=TWITTER_FRIENDS_IDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user_id in page:
                self.twack_data.add_my_friend_with_user_id(user_id)
            time.sleep(TWITTER_FRIENDS_IDS_API_REQUEST_SPACING_SECONDS)

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
        my_follower_ids = self.load_followers()
        my_friend_ids = self.load_friends()
        follow_backs = set(my_follower_ids).intersection(my_friend_ids)
        return follow_backs

    def load_unfriendly_friends(self):
        my_friend_ids = self.load_friends()
        follow_backs = self.load_follow_backs()
        unfriendly = set(my_friend_ids).difference(follow_backs)
        return unfriendly

if __name__ == '__main__':
    status = MyStatus()
    my_follower_ids = status.load_followers()
    my_friend_ids = status.load_friends()
    follow_backs = status.load_follow_backs()
    unfriendly = status.load_unfriendly_friends()

    print('{0} friends, {1} followers, {2} follow-backs, {3} unfriendlies'.format(
        len(my_friend_ids), len(my_follower_ids), len(follow_backs),
        len(unfriendly)
    ))
