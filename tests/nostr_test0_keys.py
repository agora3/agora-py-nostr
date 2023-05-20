from agama_nostr.tools import get_nostr_key, print_head
from agama_nostr.client import Client 


NOSTR_SEC = get_nostr_key()
print_head("defaul setup")
nostr_client = Client(NOSTR_SEC)


print_head("create new (temporary) user")
nostr_client.new_key_generate()
