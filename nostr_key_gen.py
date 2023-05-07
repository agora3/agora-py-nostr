"""
--- agama_nostr LIB --- 2023

Initializing a new key for your nostr "account".
Put the generated NOSTR_SEC into the key file: ./agama_nostr/nostr_key.py

...and keep it carefully.
"""

from agama_nostr.tools import print_head, new_key_generate


print_head("new_key_generate")

pub, sec = new_key_generate(False)
print("new pub.key:", pub)
print("NOSTR_SEC =>",sec)
print()
print("(you can save the NOSTR_SEC key in the file: ./agama_nostr/nostr_key.py)\n")
