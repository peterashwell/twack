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

create table friend_attempt (
    id integer primary key,
    user_id integer,
    timestamp string default now
);

create table favorite_attempt (
	id integer primary key,
	user_id integer,
	tweet_id_favorited integer,
	timestamp string default now
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
