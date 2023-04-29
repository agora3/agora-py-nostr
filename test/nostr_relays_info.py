import json
from datetime import datetime
from agama_nostr.tools import get_relay_information, print_head, short_str
# from pynostr.relay_list import RelayList
from agama_nostr.relays import relays_list, relays_big_list, nip_11_struct_adv


DEBUG = True
LOG = True

logFile = "data/"+datetime.now().strftime("%Y%m%d_%H%M%Srelays.txt")

def log_to_file(str, log=LOG):
    print(str)
    if log:
        fLog = open(logFile,"a") #a
        fLog.write(str+"\n")
        fLog.close()


# relay_url = "wss://relay.damus.io"
log_to_file("relays INFO - ver.0.1/2023-04")
log_to_file("="*39)


i = 1
# for relay_url in relays_list: 
for relay_url in relays_big_list:
    h_str = str(i) + ") " +relay_url
    #print_head(str)
    log_to_file("-"*39)
    log_to_file(h_str)
    log_to_file("-"*39)
    
    i += 1
    
    relay_data = get_relay_information(relay_url)

    if DEBUG:
        print("[relay_json]")
        print("relay_data:", relay_data)
        print("[relay_dict]")
    try:
        for info in nip_11_struct_adv:
            #if info = "pubkey":
            #print("{:<11s} - {}".format(info,short_str(relay_data.get(info))))
            r_str = "{:<13s} - {}".format(info,str(relay_data.get(info)))
            log_to_file(r_str)

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

