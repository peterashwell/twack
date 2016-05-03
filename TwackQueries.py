from TwackData import TwackData


class TwackQueries:
    def __init__(self):
        self.klass = type(self).__name__
        self.twack_data = TwackData()

    def _remove_twack_users_already_following_me(self, twack_users):
        my_follower_ids = {
            f.user_id for f in self.twack_data.load_my_followers()
        }
        return list(filter(
            lambda tu: tu.user_id not in my_follower_ids,
            twack_users
        ))

    def candidates(self):
        seed_followers = self.twack_data.seed_followers_by_sum_followed()
        return self._remove_twack_users_already_following_me(seed_followers)

    def candidates_last_liked_first(self):
        """Find good candidates and sort by like attempts first

        So the next candidate will be the one whose tweets I have liked
        equal least who has the most seed followers in their friends list.
        """
        seed_followers = self.twack_data.seed_followers_by_sum_followed(
            sort_by_favorites=True
        )
        return self._remove_twack_users_already_following_me(seed_followers)

    def candidates_last_friended_first(self):
        """Find good candidates in order of last friended by me first

        After the number of friend attempts, order by seed follow count
        """
        seed_followers = self.twack_data.seed_followers_by_sum_followed(
            sort_by_friends=True
        )
        return self._remove_twack_users_already_following_me(seed_followers)

if __name__ == '__main__':
    a = TwackQueries()
    sorted_followers = a.candidates_last_liked_first()
    print('total candidates:', len(sorted_followers))
    for user in sorted_followers:
        print('candidate: {0} {1}'.format(
            user.screen_name, user.favorite_count
        ))
