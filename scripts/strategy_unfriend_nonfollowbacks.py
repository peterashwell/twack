# Go through list of all my friends
# Unfriend those that do not follow me

from TwitterQueries import TwitterQueries
from TwitterApi import tweepy_with_auth

status = TwitterQueries()
unfriendly = status.find_unfriendly_friends()

print('script:unfollow_unfriendly | Unfriending {0} friends'.format(len(unfriendly)))

for user_id in unfriendly:
    user = tweepy_with_auth.destroy_friendship(
        user_id=user_id
    )
    print('removed friend:', user.screen_name)
