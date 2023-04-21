#!/usr/bin/env python
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC

DEBUG = True

nostr_client = Client(NOSTR_SEC)

# recipient_str = input("recipient (npub or nip05): ")
recipient_str = "npub1----your-pub-key-----"
# msg = input("message: ")
msg = "test9.2 class automatic"

nostr_client.send_mess(recipient_str, msg)
