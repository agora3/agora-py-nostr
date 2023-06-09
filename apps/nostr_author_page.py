import json
from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC, NOSTR_PUB_RELAY
from agama_nostr.tools import print_head
from agama_nostr.nips import meta_struct


DEBUG = False
nostr_client = Client(NOSTR_SEC, False)

npub1 = "npub1relay9mayryh7vnvmf5e250sskuw07fk2z6gkm585zltehlwhj9stx05lg"
author = NOSTR_PUB_RELAY

# authot-meta-info
nostr_client.set_filter_meta(author)
#nostr_client.set_subscription_id()

nostr_client.single_relay_event()
nostr_client.message_pool_events()

if DEBUG:
    print("-"*39)
    print(nostr_client.last_event_msg)
    print("-"*39)
meta_data = nostr_client.last_event_msg.content
data = json.loads(meta_data)

print("="*39)
for meta in meta_struct:
    try:
        print(meta + ":",data[meta])
    except:
        print(meta,"?")


print("="*60)
#nostr_client = Client(NOSTR_SEC)
nostr_client.set_filters(nostr_user=author,limit_num = 50)
#nostr_client.io_loop.close() # Err.Event loop is closed
#nostr_client.io_loop.clear_instance() # Err. Operation timed out after None seconds
nostr_client.io_loop.clear_current()
nostr_client.list_events_old()

###nostr_client.list_events_old()
#nostr_client.single_relay_init()
#nostr_client.io_loop_run()
#nostr_client.get_all_events_table()