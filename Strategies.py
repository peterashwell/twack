import time
import sys

import tweepy

from TwitterApi import tweepy_with_auth, TwitterConstants
from TwackQueries import TwackQueries
from TwackData import TwackData

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Strategies:
    NUMBER_TO_FOLLOW = 5000
    NUMBER_OF_TWEETS_TO_LIKE = 5000

    TWEET_LIKABILITY_FAVORITE_WEIGHT = 1
    TWEET_LIKABILITY_RETWEET_WEIGHT = 3

    def __init__(self):
        self.twack_data = TwackData()
        self.analyser = TwackQueries()

    def _tweet_likability_score(self, tweet):
        return (
            tweet.retweet_count * self.TWEET_LIKABILITY_RETWEET_WEIGHT +
            tweet.favorite_count * self.TWEET_LIKABILITY_FAVORITE_WEIGHT
        )

    def _get_best_tweet_to_like(self, tweets):
        """Return the highest scoring tweet from tweets

        Scores are points by: retweets 3 points, likes 1
        """
        if len(tweets) == 0:
            return None

        # Return the most likeable tweet
        tweets.sort(key=self._tweet_likability_score, reverse=True)
        return tweets[0]

    def destroy_all_favorites(self):
        # Dump already liked tweets
        cursor = tweepy.Cursor(
            tweepy_with_auth.favorites,
            count=TwitterConstants.FAVORITES_API_MAX_COUNT
        )
        for page in cursor.pages():
            for liked_tweet in page:
                try:
                    logger.info('Unliked tweet by {0}'.format(
                        liked_tweet.user.screen_name
                    ))
                    tweepy_with_auth.destroy_favorite(liked_tweet.id)
                except tweepy.TweepError:
                    logger.exception('Had tweeperror unliking {0}'.format(
                        liked_tweet.user.screen_name
                    ))
                except Exception:
                    logger.exception('Had exception unliking {0}'.format(
                        liked_tweet.user.screen_name
                    ))

    def _like_users_best_tweet(self, twack_user):
        # Get their tweets and ignore retweets
        tweets = tweepy_with_auth.user_timeline(twack_user.user_id)
        tweets = list(filter(
            lambda t: not hasattr(t, 'retweeted_status'), tweets
        ))

        # Find the 'best' by number of retweets and likes
        # Do nothing if they have no tweets
        best = self._get_best_tweet_to_like(tweets)
        if best is None:
            return False

        logger.info('like tweet by {0} - {1} rt {2} <3'.format(
            best.user.screen_name, best.retweet_count,
            best.favorite_count
        ))

        # Like the tweet. Ignore tweepy errors, but not real ones
        tweepy_with_auth.create_favorite(best.id)
        time.sleep(
            TwitterConstants.CREATE_FAVORITE_API_SLEEP_SECONDS
        )

        return best.id

    def gain_followers_like_strategy(self):
        """Gain followers by liking statuses of good candidates

        Good candidates are measured by how many of the seed list they follow.

        The process is to take a candidate, get their tweets, choose the best
        tweet in the last 24 hours, or otherwise their last tweet, and like it.

        Stop at amount specified by pre-determined constant
        """
        self.destroy_all_favorites()

        # Go through each candidate from people I'm not following
        candidates = self.analyser.candidates_last_liked_first()

        liked_tweet_count = 0

        for twack_user in candidates:
            try:
                liked_tweet_id = self._like_users_best_tweet(twack_user)
                liked_tweet_count += 1
                self.twack_data.add_favorite_attempt(
                    twack_user.user_id, liked_tweet_id
                )
            except tweepy.TweepError:
                # Log as attempt with 'null' tweet id recorded as what we liked
                self.twack_data.add_favorite_attempt(
                    twack_user.user_id, -1
                )
                logger.exception('TweepError liking {0} tweet'.format(
                    twack_user.screen_name
                ))
            except Exception:
                logger.exception('Exception liking {0} tweet'.format(
                    twack_user.screen_name
                ))

            if liked_tweet_count > self.NUMBER_OF_TWEETS_TO_LIKE:
                break

    def _add_twack_user_as_friend(self, twack_user):
        tweepy_with_auth.create_friendship(twack_user.user_id)
        logger.info('following {0}'.format(twack_user.screen_name))
        time.sleep(TwitterConstants.CREATE_FRIENDSHIP_API_SLEEP_SECONDS)

    def _remove_twack_users_already_my_friends(self, twack_users):
        my_friends_ids = {
            f.user_id for f in self.twack_data.load_my_friends()
        }
        return list(filter(
            lambda c: c.user_id not in my_friends_ids,
            twack_users
        ))

    def gain_followers_friends_strategy(self):
        """Gain followers by friending people who are likely to follow back

        Friend first people who have followed a large number of the seed list.
        Do not follow people who are already my friends, and ignore errors.
        Keep going until the given limit (NUMBER_TO_FOLLOW) is reached.
        """
        candidates = self._remove_twack_users_already_my_friends(
            self.analyser.candidates_last_friended_first()
        )

        successful_follow_count = 0
        for candidate in candidates:
            try:
                self._add_twack_user_as_friend(candidate)
                self.twack_data.add_friend_attempt(candidate.user_id)
                successful_follow_count += 1
            except tweepy.TweepError:
                self.twack_data.add_friend_attempt(candidate.user_id)
                logger.exception('TweepError adding {0} as friend'.format(
                    candidate.screen_name
                ))
            except Exception:
                logger.exception('Exception adding {0} as friend'.format(
                    candidate.screen_name
                ))

            if successful_follow_count > self.NUMBER_TO_FOLLOW:
                logger.info('Reached add friend limit')
                break
