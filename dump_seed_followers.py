import json
import os
import time

import tweepy

from Meta import seed_screen_names
from Auth import tweepy_with_auth

TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS = 60
TWITTER_FOLLOWERS_API_MAX_COUNT = 200
TWACK_DUMP_PATH = os.environ['TWACK_FOLLOWER_DUMP_PATH']

for seed_screen_name in seed_screen_names:
    cursor = tweepy.Cursor(
        tweepy_with_auth.followers,
        screen_name=seed_screen_name,
        count=TWITTER_FOLLOWERS_API_MAX_COUNT
    )

    for page in cursor.pages():
        for user in page:
            blob = {
                'follower_of': seed_screen_name,
                'user': user._json,
                'scraped_at': int(time.time())
            }
            dump_path = os.path.join(
                TWACK_DUMP_PATH, '{0}.json'.format(user.screen_name)
            )
            with open(dump_path, 'w') as dump_file:
                dump_file.write(json.dumps(blob))
        time.sleep(TWITTER_FOLLOWERS_API_REQUEST_SPACING_SECONDS)
