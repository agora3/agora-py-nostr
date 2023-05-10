from time import sleep
from datetime import datetime
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC,False)

print_head("new_key_generate")
pub, sec = nostr_client.new_key_generate(False)
print(pub)
print("NOSTR_SEC =",sec)


