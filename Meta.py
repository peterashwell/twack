import os

class Meta:
    seed_screen_names_path = os.path.join(
        'data', 'seed_screen_names_part2.txt'
    )
    my_screen_name = os.environ['TWACK_MY_TWITTER_SCREEN_NAME']
    my_followers_path = os.environ['TWACK_MY_FOLLOWER_IDS_PATH']
    my_friends_path = os.environ['TWACK_MY_FRIEND_IDS_PATH']

    with open(seed_screen_names_path) as seed_screen_names_file:
        seed_screen_names = list(map(
            str.strip,
            seed_screen_names_file.readlines()
        ))
