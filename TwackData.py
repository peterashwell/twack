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

    def add_twitter_user_list(self, twack_twitter_user_list):
        """Add every twack_twitter_user in the given list
        """

        query = '''
            insert into twitter_user
            (id, user_id, screen_name, followers_count,
            friends_count, blob)
            values (?, ?, ?, ?, ?, ?)
        '''
        users_padded_for_primary_keys = [
            [None] + list(user) for user in twack_twitter_user_list
        ]

        cursor = self.db.cursor()
        cursor.executemany(query, users_padded_for_primary_keys)
        self.db.commit()

    def remove_twitter_user_list(self, twack_twitter_user_list):
        """Remove every twitter user from the given list
        """
        query_params = '({0})'.format(
            ','.join('?' * len(twack_twitter_user_list))
        )

        query = '''
            delete from twitter_user
            where user_id in
        ''' + query_params
        user_ids = [user.user_id for user in twack_twitter_user_list]

        cursor = self.db.cursor()
        cursor.execute(query, user_ids)
        self.db.commit()

    def clear_all_followers(self):
        pass

    def get_all_my_friends(self):
        pass

    def add_my_friends(self, twack_twitter_user_list):
        pass

    def clear_all_friends(self):
        pass

if __name__ == '__main__':
    twd = TwackData()

    some_list = [
        TwackTwitterUser(
            '12345', 'supscreen', 23, 56, '{"blob": "dicks"}'
        )
    ]
    twd.add_twitter_user_list(some_list)
    twd.remove_twitter_user_list(some_list)
    twd.add_twitter_user_list(some_list)
