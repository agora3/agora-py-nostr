#!/usr/bin/env python
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC


nostr_client = Client(NOSTR_SEC)

recipient_str = "npub1...recipient (npub or nip05)"
msg = "... your message ..."

nostr_client.send_mess(recipient_str, msg)
