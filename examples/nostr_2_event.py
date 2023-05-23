from time import sleep
from agama_nostr.client import Client 
# from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import get_nostr_key, print_head


NOSTR_SEC = get_nostr_key() 
nc = Client(NOSTR_SEC) # nostr client

#nc.relay_list()
#nc.subscription(limit_num=20)

print_head("test: send event")
nc.simple_event(txt="Hello Nostr! \nThis is a message sent from the very simple python client Agama_nostr.\nTest")

sleep(1)
nc.list_events(limit_num=10)
