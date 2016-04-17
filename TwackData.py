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

    def add_follow_attempt(self, twack_twitter_user):
        pass

    def delete_all_my_followers(self):
        """Delete everything from my_followers table
        """
        query = '''
            delete from my_followers
        '''
        self.db.cursor().execute(query)
        self.db.commit()

    def delete_all_my_friends(self):
        """Delete everything from my_friends table
        """
        query = '''
            delete from my_friends
        '''
        self.db.cursor().execute(query)
        self.db.commit()

    def add_my_follower_with_user_id(self, user_id):
        """Add a twack twitter user as a follower of mine
        """
        query = '''
            insert into my_followers
            (user_id)
            values (?)
        '''

        self.db.cursor().execute(
            query, (user_id,)
        )
        self.db.commit()

    def add_my_friend_with_user_id(self, user_id):
        """Add a twack twitter user as a friend of mine
        """
        query = '''
            insert into my_friends
            (user_id) values (?)
        '''

        self.db.cursor().execute(
            query, (user_id,)
        )
        self.db.commit()

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
