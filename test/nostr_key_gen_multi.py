from time import sleep
from datetime import datetime
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC
from agama_nostr.tools import print_head


nostr_client = Client(NOSTR_SEC)


find_strings = ["1test", "..." ]


logFile = "data/"+datetime.now().strftime("%Y%m%d_%H%M%Slog.txt")

def log_to_file(co):
    fLog = open(logFile,"a") #a
    fLog.write(co+"\n")
    fLog.close()


log_to_file(find_string)
num = 10000000
log_to_file(str(num))
log_to_file("-------------")


for i in range(num):
    
    pub, sec = nostr_client.new_key_generate(False)
    #print(i, pub)
    if (i%10000==0):
        print(i, end=" ")
    
    for find_string in find_strings:
        if find_string in pub:
            print("-"*50)
            print(find_string, pub)
            print("sec", sec)
            log_to_file(find_string +": " +str(pub)+" / "+ str(sec))
            print("-"*50)
            sleep(1)

