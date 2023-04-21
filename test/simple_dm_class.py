#!/usr/bin/env python
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC

DEBUG = True

nostr_client = Client(NOSTR_SEC)

recipient_str = input("recipient (npub or nip05): ")
msg = input("message: ")
    
nostr_client.send_mess(recipient_str, msg)



"""
    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    io_loop.stop()
"""