"""
--- agama_nostr LIB --- 2023
Initializing a new key for your nostr "account".
...and keep it carefully.
"""
from agama_nostr.tools import print_head, new_key_generate


print_head("new_key_generate")

pub, sec = new_key_generate(False)
print("new pub.key:", pub)
print("NOSTR_SEC =>",sec)
print()
print("(you can save as the NOSTR_KEY in the file .env)\n")

"""
$ python3 nostr_key_gen.py

---------------------------------------
----- new_key_generate
---------------------------------------
new pub.key: npub1ag0ra0shs0s...z68qqq2jgj
NOSTR_SEC => 98b7b......................................................7a1f5

(you can save as the NOSTR_KEY in the file .env)
"""
