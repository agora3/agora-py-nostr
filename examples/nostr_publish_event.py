from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC


nostr_client = Client(NOSTR_SEC, False)
nostr_client.connect_to_relay()
nostr_client.publish_event(txt="Hello Nostr! \nHave a nice day.\n")
sleep(1)

#relay = "wss://relay.damus.io"
#nostr_client.set_filters()
#nostr_client.publish_event(txt="Hello Nostr! \nHave a nice day.\n",relay=relay)

#nostr_client.list_events(limit_num=10)
