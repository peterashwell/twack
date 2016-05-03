import time
import sys

import tweepy

from Auth import tweepy_with_auth
from Analyse import Analyse
from TwackData import TwackData

import logging
logger = logging.getLogger(__name__)


class Strategies:
    TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS = 10
    TWITTER_CREATE_FAVORITE_API_REQUEST_SPACING_SECONDS = 20
    TWITTER_FAVORITES_API_MAX_COUNT = 200
    NUMBER_TO_FOLLOW = 500
    NUMBER_OF_TWEETS_TO_LIKE = 5000

    def __init__(self):
        self.twack_data = TwackData()
        self.analyser = Analyse()

    def _get_best_tweet_to_like(self, tweets):
        """Return the highest scoring tweet from tweets

        Scores are points by: retweets 3 points, likes 1
        """

        FAVORITE_WEIGHT = 1
        RETWEET_WEIGHT = 3

        if len(tweets) == 0:
            return None

        def tweet_likability_score(tweet):
            return (
                tweet.retweet_count * RETWEET_WEIGHT +
                tweet.favorite_count * FAVORITE_WEIGHT
            )

        # Sort the tweets, highest scores first
        tweets.sort(key=tweet_likability_score, reverse=True)

        return tweets[0]

    def destroy_all_favorites(self):
        # Dump already liked tweets
        cursor = tweepy.Cursor(
            tweepy_with_auth.favorites,
            count=self.TWITTER_FAVORITES_API_MAX_COUNT
        )
        for page in cursor.pages():
            for liked_tweet in page:
                try:
                    logger.info('Actions | unlike tweet by {0}'.format(
                        liked_tweet.user.screen_name
                    ))
                    tweepy_with_auth.destroy_favorite(liked_tweet.id)
                except tweepy.TweepError as e:
                    logger.exception('Encountered a tweepy error unliking tweet by {0}'.format(
                        liked_tweet.user.screen_name
                    ))
                except Exception:
                    logger.exception('Encountered a problem unliking tweet by {0}'.format(
                        liked_tweet.user.screen_name
                    ))

    def gain_followers_like_strategy(self):
        """Gain followers by liking statuses of good candidates

        Good candidates are measured by how many of the seed list they follow.

        The process is to take a candidate, get their tweets, choose the best
        tweet in the last 24 hours, or otherwise their last tweet, and like it.

        Stop at NUMBER_TO_LIKE amount
        """
        self.destroy_all_favorites()

        # Go through each candidate from people I'm not following
        candidates = self.analyser.good_candidates_not_following_me_last_liked_first()
        already_liked_tweet_ids = {
            t.id for t in tweepy_with_auth.favorites()
        }

        liked_tweet_count = 0

        for c in candidates:
            try:
                # Get their tweets
                tweets = tweepy_with_auth.user_timeline(c.user_id)
                tweets = list(filter(
                    lambda t: not hasattr(t, 'retweeted_status'), tweets
                ))

                # Find the 'best' by number of retweets and likes
                best = self._get_best_tweet_to_like(tweets)

                # Skip this user if we already liked their best tweet
                if best is None or best.id in already_liked_tweet_ids:
                    continue

                logger.info('Actions | like tweet by {0} - {1} rt {2} <3'.format(
                    best.user.screen_name, best.retweet_count, best.favorite_count
                ))

                # Like the tweet. Ignore tweepy errors, but not real ones
                tweepy_with_auth.create_favorite(best.id)
                liked_tweet_count += 1

                self.twack_data.add_favorite_attempt(
                    c.user_id, best.id
                )
                time.sleep(
                    self.TWITTER_CREATE_FAVORITE_API_REQUEST_SPACING_SECONDS
                )

            except tweepy.TweepError as e:
                self.twack_data.add_favorite_attempt(
                    c.user_id, -1
                )
                logger.exception('Encountered problem liking tweet by {0}'.format(
                    c.screen_name
                ))
            except Exception as e:
                logger.exception('Encountered problem liking tweet by {0}'.format(
                    c.screen_name
                ))

            if liked_tweet_count > self.NUMBER_OF_TWEETS_TO_LIKE:
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
        candidates = list(filter(
            lambda c: c.user_id not in my_friends_ids,
            self.analyser.good_candidates_not_following_me_last_friended_first()
        ))

        successful_follow_count = 0
        for candidate in candidates:
            user_id = candidate.user_id
            screen_name = candidate.screen_name
            self.twack_data.add_friend_attempt(user_id)
            try:
                tweepy_with_auth.create_friendship(user_id)
                logger.info('following {0}'.format(screen_name))
                time.sleep(
                    self.TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS
                )
                successful_follow_count += 1
            except tweepy.TweepError as e:
                logger.exception('Encountered problem adding {0} as friend'.format(
                    screen_name
                ))
            except Exception as e:
                logger.exception('Encountered problem adding {0} as friend'.format(
                    screen_name
                ))

            if successful_follow_count > self.NUMBER_TO_FOLLOW:
                logger.info('Reached limit of {0} in following people'.format(
                    self.NUMBER_TO_FOLLOW
                ))
                sys.exit(0)
