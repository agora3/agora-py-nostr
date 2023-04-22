from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC)

print_head("my relays list")
nostr_client.print_myrelays_list()

print_head("online relays list")
nostr_client.scann_relay_list()
