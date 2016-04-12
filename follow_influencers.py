from Auth import tweepy_with_auth
from Analyse import Analyse

# Load list of influencers and list of people I follow
# then start following those not already following me
# keep going until twitter API forbids further follows

influencers = Analyse.get_sorted_followers()
