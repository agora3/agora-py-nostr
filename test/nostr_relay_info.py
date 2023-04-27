import json
from agama_nostr.tools import get_relay_information, print_head
# from pynostr.relay_list import RelayList
from agama_nostr.relays import relays_list

# relay_url = "wss://relay.damus.io"

for relay_url in relays_list:
    print_head(relay_url)
    try:
        json_str = get_relay_information(relay_url)
        print(len(json_str),json_str)
        #data = json.loads(json_str)
        #print(data)
    
        for data in json_str:
            #    table.add_row([key, value])
            print(data)
    except:
        print("Err. get_relay_information")

"""
{'id': 'wss://nostr.mnethome.de/', 
'name': 'nostr-rs-relay mnethome', 
'description': 'A nostr relay.', 
'pubkey': 'npub1lx349k625y27chfnq4qdmgmmw83yvrxq7e0rxx868vjyj3wu36uqtdck4m', 
'supported_nips': [1, 2, 9, 11, 12, 15, 16, 20, 22], 
'software': 'https://git.sr.ht/~gheartsfield/nostr-rs-relay', 
'version': '0.7.17', 'url': 'wss://nostr.mnethome.de'}
"""