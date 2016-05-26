from TwitterQueries import TwitterQueries
from TwackData import TwackData

td = TwackData()
status = TwitterQueries()

# Delete currently known seed followers, then rebuild list
#td.delete_all_seed_followers()
status.dump_seed_followers()
