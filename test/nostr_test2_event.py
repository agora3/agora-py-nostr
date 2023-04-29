from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC)

#nostr_client.relay_list()
#nostr_client.subscription(limit_num=20)

print_head("test: send event")
nostr_client.simple_event(txt="Hello Nostr! \nThis is a message sent from the very simple python client Agama_nostr.\nNo.3")

sleep(1)
nostr_client.list_events(limit_num=10)
