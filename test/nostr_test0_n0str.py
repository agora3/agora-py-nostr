from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC, NOSTR_SEC_N0STR2, NOSTR_SEC_N0STR5
from agama_nostr.tools import print_head


print_head("defaul setup")
nostr_client = Client(NOSTR_SEC)


print_head("NOSTRi")
nostr_client = Client(NOSTR_SEC_N0STR2, relays=False)

nostr_client = Client(NOSTR_SEC_N0STR5, relays=False)


print_head("create new (temporary) user")
nostr_client.new_key_generate()