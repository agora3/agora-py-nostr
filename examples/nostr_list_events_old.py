import datetime, time
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC)

"""
current_timestamp = time.time()
one_month_from_now = datetime.datetime.fromtimestamp(current_timestamp) + datetime.timedelta(days=30)
one_month_from_now_timestamp = int(one_month_from_now.timestamp())
print("one_month_from_now_timestamp",one_month_from_now_timestamp) # 1686200000
"""

print_head("list_events - table")

nostr_client.set_filters(limit_num = 5)
#nostr_client.list_events()
nostr_client.list_events_old()
