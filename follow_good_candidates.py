import time

from tweepy import TweepError

from Auth import tweepy_with_auth
from Analyse import Analyse
from TwackData import TwackData

# Load list of candidates and list of people I follow
# then start following those not already following me
# keep going until twitter API forbids further follows

TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS = 10

twack_data = TwackData()
analyser = Analyse()

my_friends_ids = {f.user_id for f in twack_data.load_my_friends()}
candidates = analyser.good_candidates_not_already_following()

NUMBER_TO_FOLLOW = 100

successful_follow_count = 0
for candidate in candidates:
    if successful_follow_count > NUMBER_TO_FOLLOW:
        print('script:follow_good_candidates | reached {0} limit'.format(NUMBER_TO_FOLLOW))
        break

    try:
        user_id = candidate.user_id
        if user_id not in my_friends_ids:
            tweepy_with_auth.create_friendship(user_id)
            print('script:follow_good_candidates | following {0}'.format(candidate.screen_name))
            time.sleep(TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS)
            successful_follow_count += 1
    except TweepError as e:
        print(e)
    except Exception as e:
        raise e
