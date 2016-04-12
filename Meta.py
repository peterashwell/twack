import os

seed_screen_names_path = os.path.join(
    'data', 'seed_screen_names.txt'
)

with open(seed_screen_names_path) as seed_screen_names_file:
    seed_screen_names = list(map(
        str.strip,
        seed_screen_names_file.readlines()
    ))
