import sys

sys.stderr = sys.stdout

from MyStatus import MyStatus

status = MyStatus()
status.dump_my_followers()
