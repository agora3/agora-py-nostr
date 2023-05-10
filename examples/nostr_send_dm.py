#!/usr/bin/env python
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC


nostr_client = Client(NOSTR_SEC, False)

recipient_str = "npub1 ... ecipient (npub or nip05) ..."
msg = "message ........"

#recipient_str = input("recipient (npub or nip05): ")
#msg = input("message: ")

print("="*39)    
nostr_client.send_direct_message(recipient_str, msg, relay="R")
