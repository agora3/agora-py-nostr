from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head

DEBUG = True
#RELAY_URL = "wss://relay.damus.io"

nostr_client = Client(NOSTR_SEC)

print_head("my relays list")
nostr_client.print_myrelays_list()


private_key = nostr_client.private_key
public_key =  private_key.public_key
print(f"Private key: {private_key.bech32()}")
print(f"Public key: {public_key.bech32()}")


print("[2-connect-to-single-relay]")
#nostr_client.filters =  FiltersList([Filters(authors=[private_key.public_key.hex()],kinds=[EventKind.SET_METADATA])])
#nostr_client.set_filter_meta("npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj")
nostr_client.set_filter_meta()

#nostr_client.subscription_id = uuid.uuid1().hex
nostr_client.set_subscription_id()


print("[3-message-pool]")
nostr_client.single_relay_event()
"""
index = 0
if DEBUG: print("[notices]")
while message_pool.has_notices():
    if DEBUG: print("has_notices [index]", index)
    notice_msg = message_pool.get_notice()
    print(notice_msg.content)
    index += 1

"""
index = 0
if DEBUG: print("[events]")    
while nostr_client.message_pool.has_events():
    if DEBUG: print("has_events [index]", index)
    event_msg = nostr_client.message_pool.get_event()
    print(event_msg.event.content)
    index += 1

