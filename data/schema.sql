create table twitter_user (
    id integer primary key,
    user_id string,
    screen_name string,
    followers_count integer,
    friends_count integer,
    blob string,
    unique(user_id) on conflict ignore
);

create table seed_followers (
    id integer primary key,
    user_id integer,
    follower_of_screen_name string,
    unique(user_id, follower_of_screen_name) on conflict ignore
);

create table follow_attempts (
    id integer primary key,
    user_id integer,
    attempt_date string
);

create table my_followers (
    id integer primary_key,
    user_id integer,
    unique(user_id) on conflict ignore
);

create table my_friends (
    id integer primary_key,
    user_id integer,
    unique(user_id) on conflict ignore
);
