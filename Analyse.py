from collections import namedtuple
import glob
import json
import os

UserWithScore = namedtuple(
    'FollowerWithScore', 'user, score'
)


class Analyse:
    def __init__(self):
        self.klass = type(self).__name__
        dump_path = os.path.join(
            os.environ['TWACK_INFLUENCER_FOLLOWER_DUMP_PATH'], '*.json'
        )
        self.file_paths = glob.glob(dump_path)

    def compute_user_score(self, user):
        followers = user['followers_count']
        friends = user['friends_count']

        return followers / friends

    def load_followers(self):
        print('{0} | loading {1} users'.format(
            self.klass, len(self.file_paths)
        ))

        followers = []
        for dump_file_path in self.file_paths:
            with open(dump_file_path) as dump_file:
                blob = json.loads(dump_file.read())
                user = blob['user']
                score = self.compute_user_score(user)
                followers.append(UserWithScore(user, score))

        print('{0} | done loading'.format(
            len(self.file_paths)
        ))

        return followers

    def sort_followers(self, followers):
        return sorted(
            followers, key=lambda f: f.score, reverse=True
        )

    def get_sorted_followers(self):
        followers_with_scores = self.sort_followers(self.load_followers())
        return list(map(
            lambda fws: fws.user,
            followers_with_scores
        ))

if __name__ == '__main__':
    a = Analyse()
    sorted_followers = a.get_sorted_followers()
    print('total followers:', len(sorted_followers))
    for user in sorted_followers:
        print('influencer: {0} ({1}/{2})'.format(
            user['screen_name'], user['followers_count'], user['friends_count']
        ))
