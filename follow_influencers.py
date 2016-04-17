import time

from Auth import tweepy_with_auth
from Analyse import Analyse
from MyStatus import MyStatus

# Load list of influencers and list of people I follow
# then start following those not already following me
# keep going until twitter API forbids further follows

TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS = 10

my_status = MyStatus()
analyser = Analyse()

my_follower_ids = set(my_status.load_followers())
influencers = analyser.get_sorted_followers()

for influencer in influencers:
    try:
        user_id = influencer['id_str']
        if user_id not in my_follower_ids:
            tweepy_with_auth.create_friendship(user_id)
            print('script:follow_influencers | following {0}'.format(influencer['screen_name']))
            time.sleep(TWITTER_CREATE_FRIENDSHIP_API_REQUEST_SPACING_SECONDS)
    except Exception:
        print('got an error lol')
