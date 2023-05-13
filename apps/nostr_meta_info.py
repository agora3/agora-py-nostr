import json
from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head
from agama_nostr.nips import meta_struct


DEBUG = True
nostr_client = Client(NOSTR_SEC)

#print_head("my relays list")
#nostr_client.print_myrelays_list()

#npub1 = "npub1.........user id.................... "
npub1 = "npub1relay9mayryh7vnvmf5e250sskuw07fk2z6gkm585zltehlwhj9stx05lg"

nostr_client.set_filter_meta(npub1)
nostr_client.set_subscription_id()

nostr_client.single_relay_event()
nostr_client.message_pool_events()

if DEBUG:
    print("-"*39)
    print(nostr_client.last_event_msg)
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
