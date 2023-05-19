import os, sys
from time import sleep
from dotenv import load_dotenv

from agama_nostr.client import Client 

load_dotenv()  # take environment variables from .env.

if not os.environ.get('NOSTR_KEY'):
    print("You need to set NOSTR_KEY in .env file")
    sys.exit(1)

nostr_client = Client(os.environ['NOSTR_KEY'], False)
nostr_client.connect_to_relay()
nostr_client.publish_event(txt="Hello Nostr! \nHave a nice day.\n")
sleep(1)

#relay = "wss://relay.damus.io"
#nostr_client.set_filters()
#nostr_client.publish_event(txt="Hello Nostr! \nHave a nice day.\n",relay=relay)

#nostr_client.list_events(limit_num=10)
