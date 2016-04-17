# Go through list of all my friends
# Unfriend those that do not follow me

from MyStatus import MyStatus
from Auth import tweepy_with_auth

status = MyStatus()
status.dump_seed_followers()
