import sys

sys.stderr = sys.stdout

# Go through list of all my friends
# Unfriend those that do not follow me

from MyStatus import MyStatus
from Auth import tweepy_with_auth

td = TwackData()
status = MyStatus()

td.delete_all_seed_followers()
status.dump_seed_followers()
