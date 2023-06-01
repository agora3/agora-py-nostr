# export PYTHONPATH="$PYTHONPATH:./"

from agama_nostr.tools import get_nostr_key, print_head
from agama_nostr.client import Client 


NOSTR_SEC = get_nostr_key()
print_head("defaul setup")
nc = Client(NOSTR_SEC) # nostr client


print_head("create new (temporary) user")
nc.new_key_generate()
