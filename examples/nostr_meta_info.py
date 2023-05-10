from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC)

print_head("my relays list")
nostr_client.print_myrelays_list()

#private_key = nostr_client.private_key
#public_key =  private_key.public_key
#print(f"Private key: {private_key.bech32()}")
#print(f"Public key: {public_key.bech32()}")


npub1 = "npub1.........user id.................... "
nostr_client.set_filter_meta(npub1)
nostr_client.set_subscription_id()
nostr_client.single_relay_event()


print("[message-pool]")
while nostr_client.message_pool.has_events():
    event_msg = nostr_client.message_pool.get_event()
    print(event_msg.event.content)


"""
info
"""
