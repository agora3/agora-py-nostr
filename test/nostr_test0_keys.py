from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


print_head("defaul setup")
nostr_client = Client(NOSTR_SEC)


print_head("create new (temporary) user")
nostr_client.new_key_generate()
