from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC


DEBUG = True

nostr_client = Client(NOSTR_SEC)

nostr_client.subscription(limit_num=20)

print("="*50)
nostr_client.simple_event(txt="Hello Nostr! (Python Lib. pynostr) 2")
print("="*50)

sleep(5)
nostr_client.list_events(limit_num=50)
