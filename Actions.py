import time

from tweepy import TweepError

from Auth import tweepy_with_auth
from Analyse import Analyse
from TwackData import TwackData


class Actions:
    TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS = 10
    TWITTER_CREATE_FAVORITE_API_REQUEST_SPACING_SECONDS = 100
    NUMBER_TO_FOLLOW = 100
    NUMBER_OF_TWEETS_TO_LIKE = 200

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

        def tweet_likeability_score(tweet):
            return (
                tweet.retweet_count * RETWEET_WEIGHT +
                tweet.favorite_count * FAVORITE_WEIGHT
            )

        # Sort the tweets, highest scores first
        tweets.sort(key=tweet_likeability_score, reverse=True)

        return tweets[0]

    def unfavorite_all_tweets_i_like(self):
        # Dump already liked tweets
        already_liked_tweets = tweepy_with_auth.favorites()
        for liked_tweet in already_liked_tweets:
            print('Actions | unlike tweet by {0}'.format(
                liked_tweet.user.screen_name
            ))
            tweepy_with_auth.destroy_favorite(liked_tweet.id)

    def gain_followers_like_strategy(self):
        """Gain followers by liking statuses of good candidates

        Good candidates are measured by how many of the seed list they follow.

        The process is to take a candidate, get their tweets, choose the best
        tweet in the last 24 hours, or otherwise their last tweet, and like it.

        Stop at NUMBER_TO_LIKE amount
        """
        # Go through each candidate from people I'm not following
        candidates = self.analyser.good_candidates_not_following_me()
        liked_tweet_count = 0

        for c in candidates:
            # Get their tweets
            tweets = tweepy_with_auth.user_timeline(c.user_id)
            tweets = list(filter(
                lambda t: not hasattr(t, 'retweeted_status'), tweets
            ))

            # Find the 'best' by number of retweets and likes
            best = self._get_best_tweet_to_like(tweets)
            print('Actions | like tweet by {0} - {1} rt {2} <3'.format(
                best.user.screen_name, best.retweet_count, best.favorite_count
            ))

            # Like the tweet. Ignore tweepy errors, but not real ones
            try:
                tweepy_with_auth.create_favorite(best.id)
                liked_tweet_count += 1
            except TweepError as e:
                print(e)
            except Exception as e:
                raise e

            if liked_tweet_count > self.NUMBER_OF_TWEETS_TO_LIKE:
                return

            time.sleep(
                self.TWITTER_CREATE_FAVORITE_API_REQUEST_SPACING_SECONDS
            )

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
