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

    def good_candidates_not_following_me(self):
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

    def good_candidates_not_following_me_last_liked_first(self):
        """Find good candidates and sort by like attempts first

        So the next candidate will be the one whose tweets I have liked
        equal least who has the most seed followers in their friends list.
        """
        seed_followers = self.twack_data.seed_followers_by_sum_followed(
            sort_by_favorites=True
        )
        already_following_me = {
            f.user_id for f in self.twack_data.load_my_followers()
        }

        return list(filter(
            lambda f: f.user_id not in already_following_me,
            seed_followers
        ))

if __name__ == '__main__':
    a = Analyse()
    sorted_followers = a.good_candidates_not_following_me_last_liked_first()
    print('total candidates:', len(sorted_followers))
    for user in sorted_followers:
        print('candidate: {0} {1}'.format( user.screen_name, user.favorite_count))
