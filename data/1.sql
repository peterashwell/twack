create table favorite_attempt (
	id integer primary key,
	user_id integer,
	tweet_id_favorited integer,
	timestamp string default (datetime('now'))
);

create table friend_attempt (
    id integer primary key,
    user_id integer,
    timestamp string default (datetime('now'))
);
