import time

import tweepy

from TwitterApi import tweepy_with_auth, TwitterConstants
from Meta import Meta
from TwackData import TwackData, tweepy_user_to_twack_user


class TwitterQueries:
    def __init__(self):
        self.twack_data = TwackData()

    def dump_seed_followers(self):
        for seed_screen_name in Meta.seed_screen_names:
            cursor = tweepy.Cursor(
                tweepy_with_auth.followers,
                screen_name=seed_screen_name,
                count=TwitterConstants.FOLLOWERS_API_MAX_COUNT
            )

            for page in cursor.pages():
                for user in page:
                    twack_twitter_user = tweepy_user_to_twack_user(user)
                    self.twack_data.add_twack_twitter_user(twack_twitter_user)
                    self.twack_data.add_follower_of_screen_name(
                        twack_twitter_user, seed_screen_name
                    )
                time.sleep(
                    TwitterConstants.FOLLOWERS_API_REQUEST_SPACING_SECONDS
                )

    def dump_my_followers(self):
        twack_data = TwackData()
        twack_data.delete_all_my_followers()

        cursor = tweepy.Cursor(
            tweepy_with_auth.followers,
            screen_name=Meta.my_screen_name,
            count=TwitterConstants.FOLLOWERS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user in page:
                twack_twitter_user = tweepy_user_to_twack_user(user)
                twack_data.add_twack_twitter_user(twack_twitter_user)
                twack_data.add_my_follower(twack_twitter_user)
            time.sleep(
                TwitterConstants.FOLLOWERS_API_REQUEST_SPACING_SECONDS
            )

    def dump_my_friends(self):
        twack_data = TwackData()
        twack_data.delete_all_my_friends()

        cursor = tweepy.Cursor(
            tweepy_with_auth.friends,
            screen_name=Meta.my_screen_name,
            count=TwitterConstants.FRIENDS_API_MAX_COUNT
        )
        for page in cursor.pages():
            for user in page:
                twack_twitter_user = tweepy_user_to_twack_user(user)
                twack_data.add_twack_twitter_user(twack_twitter_user)
                twack_data.add_my_friend(twack_twitter_user)
            time.sleep(
                TwitterConstants.FRIENDS_API_REQUEST_SPACING_SECONDS
            )

    def find_unfriendly_friends(self):
        twack_data = TwackData()

        my_followers = twack_data.load_my_followers()
        my_friends = twack_data.load_my_friends()

        my_followers_ids = {f.user_id for f in my_followers}
        my_friends_ids = {f.user_id for f in my_friends}

        unfriendly = my_friends_ids.difference(my_followers_ids)
        return unfriendly

if __name__ == '__main__':
    status = TwitterQueries()
    tw = TwackData()

    my_followers = tw.load_my_followers()
    my_friends = tw.load_my_friends()
    unfriendly = status.find_unfriendly_friends()

    print('{0} friends, {1} followers, {2} unfriendlies'.format(
        len(my_friends), len(my_followers), len(unfriendly)
    ))
