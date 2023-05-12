import json
from datetime import datetime
from agama_nostr.tools import get_relay_information, print_head, short_str
from agama_nostr.relays import relays_list100 , relays_big_list
from agama_nostr.nips import nip_11_struct_adv


DEBUG = True
LOG = True

#---test---
#>>> len(relays_big_list)
#277 

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
for relay_url in relays_list100:
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
