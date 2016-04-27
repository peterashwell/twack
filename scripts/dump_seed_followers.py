from MyStatus import MyStatus
from TwackData import TwackData

td = TwackData()
status = MyStatus()

# Delete currently known seed followers, then rebuild list
td.delete_all_seed_followers()
status.dump_seed_followers()
