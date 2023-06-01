import datetime, time
from agama_nostr.client import Client 
from agama_nostr.tools import get_nostr_key, print_head


NOSTR_SEC = get_nostr_key() 
nc = Client(NOSTR_SEC) # nostr_client


print_head("list_events - table")

nc.set_filters(limit_num = 10)
#nostr_client.list_events()
nc.list_events_old()
