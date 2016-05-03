import sys

sys.stderr = sys.stdout

from TwitterQueries import TwitterQueries

status = TwitterQueries()
status.dump_my_followers()
status.dump_my_friends()
