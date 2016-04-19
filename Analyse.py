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

    def good_candidates_not_already_following(self):
        seed_followers = self.twack_data.seed_followers_by_sum_followed()
        print('{0} | loading {1} users'.format(
            self.klass, len(seed_followers)
        ))
        my_followers = self.twack_data.load_my_followers()
        already_following_me = {f.user_id for f in my_followers}

        not_already_following = filter(
            lambda f: f.user_id not in already_following_me, seed_followers
        )
        return list(not_already_following)

if __name__ == '__main__':
    a = Analyse()
    sorted_followers = a.good_candidates_not_already_following()
    print('total candidates:', len(sorted_followers))
    for user in sorted_followers:
        print('candidate: {0}'.format(
            user.screen_name
        ))
