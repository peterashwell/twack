with open('seed_screen_names.txt') as seed_screen_names_file:
    seed_screen_names = list(map(
        str.strip,
        seed_screen_names_file.readlines()
    ))
