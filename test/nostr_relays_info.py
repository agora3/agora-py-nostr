import json
from agama_nostr.tools import get_relay_information, print_head, short_str
# from pynostr.relay_list import RelayList
from agama_nostr.relays import relays_list, relays_big_list


DEBUG = True

# relay_url = "wss://relay.damus.io"

"""
 "name": <string identifying relay>,
 "description": <string with detailed information>,
 "pubkey": <administrative contact pubkey>,
 "contact": <administrative alternate contact>,
 "supported_nips": <a list of NIP numbers supported by the relay>,
 "software": <string identifying relay software URL>,
 "version": <string version identifier>
"""

nip_11_struct = [ "name","description","pubkey","contact","supported_nips","software","version","limitation"]

i = 1
for relay_url in relays_list: # relays_big_list:
    print_head(str(i) + ") " +relay_url)
    i += 1
    
    relay_data = get_relay_information(relay_url)

    if DEBUG:
        print("[relay_json]")
        print("relay_data:", relay_data)
        print("[relay_dict]")
    try:
        for info in nip_11_struct:
            #if info = "pubkey":
            #print("{:<11s} - {}".format(info,short_str(relay_data.get(info))))
            print("{:<13s} - {}".format(info,str(relay_data.get(info))))

        #relay_dict = json.loads(relay_data )
        #print(relay_dict)
    except:
            print("Err. parse relay_data")
    #except:
    #    print("Err. get_relay_information")

"""
{'id': 'wss://nostr.mnethome.de/', 
'name': 'nostr-rs-relay mnethome', 
'description': 'A nostr relay.', 
'pubkey': 'npub1lx349k625y27chfnq4qdmgmmw83yvrxq7e0rxx868vjyj3wu36uqtdck4m', 
'supported_nips': [1, 2, 9, 11, 12, 15, 16, 20, 22], 
'software': 'https://git.sr.ht/~gheartsfield/nostr-rs-relay', 
'version': '0.7.17', 'url': 'wss://nostr.mnethome.de'}

---------------------------------------
----- wss://relay.damus.io
---------------------------------------
name          - damus.io 
description   - Damus strfry relay
pubkey        - 32e1827635450ebb3c5a7d12c1f8e7b2b514439ac10a67eef3d9fd9c5c68e245
contact       - jb55@jb55.com
supported_nips - [1, 9, 11, 12, 15, 16, 20, 22]
software      - git+https://github.com/hoytech/strfry.git
version       - v78-30b8c38

"""

