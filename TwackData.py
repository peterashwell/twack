import os
import sqlite3

from collections import namedtuple

TwackTwitterUser = namedtuple(
    'TwackTwitterUser',
    'user_id, screen_name, followers_count, friends_count, blob'
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

    def get_all_my_followers(self):
        pass

    def add_twitter_user_list_as_followers(self):
        pass

    def add_follower_of_screen_name(self, twack_twitter_user, screen_name):
        """Add a follower relationship with screen_name
        """
        query = '''
            insert into seed_followers
            (user_id, follower_of_screen_name)
            values (?, ?)
        '''

        self.db.cursor().execute(
            query, (twack_twitter_user.user_id, screen_name)
        )
        self.db.commit()

    def add_twack_twitter_user(self, twack_twitter_user):
        """Add a single twack_twitter_user
        """

        query = '''
            insert into twitter_user
            (id, user_id, screen_name, followers_count,
            friends_count, blob)
            values (?, ?, ?, ?, ?, ?)
        '''

        # Pad with None for primary key field
        twack_twitter_user = [None] + list(twack_twitter_user)

        cursor = self.db.cursor()
        cursor.execute(query, twack_twitter_user)
        self.db.commit()

    def remove_twack_twitter_user(self, twack_twitter_user):
        """Remove a single twack twitter user (by twitter id)
        """
        query = '''
            delete from twitter_user
            where user_id = ?
        '''

        cursor = self.db.cursor()
        cursor.execute(query, (twack_twitter_user.user_id,))
        self.db.commit()

    def clear_all_followers(self):
        pass

    def get_all_my_friends(self):
        pass

    def add_my_friends(self, twack_twitter_users):
        pass

    def clear_all_friends(self):
        pass

if __name__ == '__main__':
    twd = TwackData()

    some_user = TwackTwitterUser(
        '12345', 'supscreen', 23, 56, '{"blob": "dicks"}'
    )
    some_list = [some_user]

    twd.add_twack_twitter_users(some_list)
    twd.remove_twack_twitter_users(some_list)
    twd.add_twack_twitter_users(some_list)

    twd.add_twack_twitter_user(some_user)
    twd.remove_twack_twitter_user(some_user)
    twd.add_twack_twitter_user(some_user)

    twd.add_follower_of_screen_name(some_user, 'crypto_god')
