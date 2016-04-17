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

    def seed_followers_by_sum_seeds_followed(self):
        query = '''
            select tu.user_id, tu.screen_name, tu.followers_count,
            tu.friends_count, tu.blob, count(sf.follower_of_screen_name) as seed_count
            from seed_followers sf
            inner join twitter_user tu
            on tu.user_id = sf.user_id
            group by sf.user_id
        '''
        results = self.db.cursor().execute(query).fetchall()
        packed_results = []
        for r in results:
            user_slice = r[:-1]
            seed_count = r[-1]
            user = TwackTwitterUser._make(user_slice)
            packed_results.append((user, seed_count))
        return packed_results

    def load_my_friends(self):
        query = '''
            select tu.user_id, tu.screen_name, tu.followers_count,
            tu.friends_count, tu.blob
            from twitter_user tu
            inner join my_friends mf on tu.user_id = mf.user_id
        '''
        results = self.db.cursor().execute(query).fetchall()
        return list(map(TwackTwitterUser._make, results))

    def load_my_followers(self):
        query = '''
            select tu.user_id, tu.screen_name, tu.followers_count,
            tu.friends_count, tu.blob
            from twitter_user tu
            inner join my_followers mf on tu.user_id = mf.user_id
        '''
        results = self.db.cursor().execute(query).fetchall()
        return list(map(TwackTwitterUser._make, results))

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

    def add_my_follower(self, user):
        """Add a twack twitter user as a follower of mine
        """
        query = '''
            insert into my_followers
            (user_id)
            values (?)
        '''

        self.db.cursor().execute(
            query, (user.user_id,)
        )
        self.db.commit()

    def add_my_friend(self, user):
        """Add a twack twitter user as a friend of mine
        """
        query = '''
            insert into my_friends
            (user_id) values (?)
        '''

        self.db.cursor().execute(
            query, (user.user_id,)
        )
        self.db.commit()

    def add_follower_of_screen_name(self, twack_twitter_user, screen_name):
        """Add a follower relationship with screen_name
        """
        print('adding {0} as follower of {1}'.format(
            twack_twitter_user.screen_name, screen_name
        ))

        query = '''
            insert into seed_followers
            (user_id, follower_of_screen_name)
            values (?, ?)
        '''

        self.db.cursor().execute(
            query, (twack_twitter_user.user_id, screen_name)
        )
        self.db.commit()

    def delete_all_seed_followers(self):
        """Remove every seed follower
        """

        query = '''
            delete from seed_followers
        '''

        self.db.cursor().execute(query)
        self.db.commit()

    def add_twack_twitter_user(self, twack_twitter_user):
        """Add a single twack_twitter_user
        """

        print('adding twitter user {0}'.format(twack_twitter_user.screen_name))

        query = '''
            insert into twitter_user
            (id, user_id, screen_name, followers_count,
            friends_count, blob)
            values (?, ?, ?, ?, ?, ?)
        '''

        # Pad with None for primary key field
        twack_twitter_user = [None] + list(twack_twitter_user)

        print('twack_twitter_user {0}'.format(twack_twitter_user))
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

    twd.add_twack_twitter_user(some_user)
    twd.remove_twack_twitter_user(some_user)
    twd.add_twack_twitter_user(some_user)

    twd.add_follower_of_screen_name(some_user, 'crypto_god')

    seed_counts = sorted(
        twd.seed_followers_by_sum_seeds_followed(),
        key=lambda sc: sc[1],
        reverse=False
    )
    for sc in seed_counts:
        print(sc[0].screen_name, sc[1])
