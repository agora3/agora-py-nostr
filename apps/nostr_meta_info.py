import json
from time import sleep
from agama_nostr.client import Client 
from agama_nostr.tools import get_nostr_key, print_head
from agama_nostr.nips import meta_struct


DEBUG = True
NOSTR_SEC = get_nostr_key() 
nc = Client(NOSTR_SEC) # nostr_client

#print_head("my relays list")
#nc.print_myrelays_list()

npub1 = "npub1.........user id.................... "
#npub1 = "npub1relay9mayryh7vnvmf5e250sskuw07fk2z6gkm585zltehlwhj9stx05lg"

nc.set_filter_meta(npub1)
nc.set_subscription_id()

nc.single_relay_event()
nc.message_pool_events()

if DEBUG:
    print("-"*39)
    print(nc.last_event_msg)
    print("-"*39)
meta_data = nostr_client.last_event_msg.content
data = json.loads(meta_data)

#print("meta_data",data)
#print(len(data))

print("="*39)
for meta in meta_struct:
    try:
        print(meta + ":",data[meta])
    except:
        print(meta,"?")
