# Go through list of all my friends
# Unfriend those that do not follow me

from MyStatus import MyStatus
from Auth import tweepy_with_auth

status = MyStatus()
unfriendly = status.load_unfriendly_friends()

for user_id in unfriendly:
    user = tweepy_with_auth.destroy_friendship(
        user_id=user_id
    )
    print('removed friend:', user.screen_name)
