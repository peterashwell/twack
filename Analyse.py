from collections import namedtuple
import glob
import json
import os

from TwackData import TwackData

UserWithScore = namedtuple(
    'FollowerWithScore', 'user, score'
)


class Analyse:
    def __init__(self):
        self.klass = type(self).__name__
        self.twack_data = TwackData()

    def good_candidates_not_followed(self):
        seed_followers = self.twack_data.seed_followers_by_sum_followed()
        print('{0} | loading {1} users'.format(
            self.klass, len(seed_followers)
        ))
        my_followers = self.twack_data.load_my_followers()
        already_following_me = {f.user_id for f in my_followers}

        not_already_following = filter(
            lambda f: f[0].user_id not in already_following_me, seed_followers
        )

        not_following_one_seed = filter(
            lambda f: f[1] > 1, not_already_following
        )

        return list(not_following_one_seed)

if __name__ == '__main__':
    a = Analyse()
    sorted_followers = a.good_candidates_not_followed()
    print('total candidates:', len(sorted_followers))
    for user in sorted_followers:
        print('candidate: {0} {1}'.format(
            user[0].screen_name, user[1]
        ))
