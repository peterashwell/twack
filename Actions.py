import time

from tweepy import TweepError

from Auth import tweepy_with_auth
from Analyse import Analyse
from TwackData import TwackData


class Actions:
    TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS = 10
    NUMBER_TO_FOLLOW = 100

    def __init__(self):

        self.twack_data = TwackData()
        self.analyser = Analyse()
        pass

    def score_tweets(self, tweets):
        """Return the highest scoring tweet from tweets

        Scores are points by: retweets 3 points, likes 1
        """
        if len(tweets) == 0:
            return None

    def gain_followers_like_strategy(self):
        """Gain followers by liking statuses of good candidates

        Good candidates are measured by how many of the seed list they follow.

        The process is to take a candidate, get their tweets, choose the best
        tweet in the last 24 hours, or otherwise their last tweet, and like it.

        Stop at NUMBER_TO_LIKE amount
        """
        candidates = self.analyser.good_candidates_not_following_me()

        # Go through each candidate
        for c in candidates:
            # Get their tweets
            tweets = tweepy_with_auth.user_timeline(c.user_id)
            print(tweets[0])
            return

    def gain_followers_friends_strategy(self):
        """Gain followers by friending people who are likely to follow back

        Friend first people who have followed a large number of the seed list.
        Do not follow people who are already my friends, and ignore errors.
        Keep going until the given limit (NUMBER_TO_FOLLOW) is reached.
        """
        my_friends_ids = {
            f.user_id for f in self.twack_data.load_my_friends()
        }
        candidates = self.analyser.good_candidates_not_following_me()
        candidates = filter(
            candidates, lambda c: c.user_id not in my_friends_ids
        )
        successful_follow_count = 0
        for candidate in candidates:
            user_id = candidate.user_id
            screen_name = candidate.screen_name
            try:
                tweepy_with_auth.create_friendship(user_id)
                print('Actions | following {0}'.format(screen_name))
                time.sleep(
                    self.TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS
                )
                successful_follow_count += 1
            except TweepError as e:
                print(e)
            except Exception as e:
                raise e

            if successful_follow_count > self.NUMBER_TO_FOLLOW:
                print('Actions | reached limit')
                break
