# agora-py-nostr

simple Python Nostr Client

This is experimental software in early development


## Install

```
git clone https://github.com/agora3/agora-py-nostr.git
cd agora-py-nostr
python3 -m venv venv  
source venv/bin/activate
pip install -r requirements.txt
```

## First start

```
put your existing NOSTR_KEY in the .env file 

NOSTR_KEY=yourSecret123Key

or generate a new one

$ python3 nostr_key_gen.py

---------------------------------------
----- new_key_generate
---------------------------------------
new pub.key: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj
NOSTR_SEC => 98b7b......................................................7a1f5

(you can save the NOSTR_SEC key in the file .env)
``` 
 
## Publish vevent
```python
from time import sleep
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC

nc = Client(NOSTR_SEC) # nostr_client
nc.publish_event(txt="Hello Nostr! \nThis event is sent from the very simple python client Agama_nostr.\nPura vida.")
sleep(1)

nc.set_filters(limit_num = 20)
nc.list_events_old()
...
```
```
│ 2023-05-17 15:01:03 │ Block 790182 was just confirmed. The total value was    │
│                     │ ($56,053,753) for 53,889,226 sats ($14,424) in fees     │
│ 2023-05-17 15:01:03 │ 絵文字選択画面直し中テスト :astraea:                      │
│ 2023-05-17 15:01:04 │ Gm #nostr #zap #plebchain                               │
│                     │ https://nostr.build/i/95e...e1.jpg                      │
│ 2023-05-17 15:01:06 │ Hello Nostr!                                            │
│                     │ This event is sent from the very simple python client Agama_nostr.
│                     │ Agama_nostr. Pura vida.                                 │
│ 2023-05-17 15:01:07 │ Good Morning Rakan!                                     │
| 2023-05-09 11:46:21 │ インターネッコです .....
```

## Get Author Metadata info 
```python
import json
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC, NOSTR_PUB_RELAY
from agama_nostr.nips import meta_struct

nc = Client(NOSTR_SEC, False) # nostr_client
nc.set_filter_meta(NOSTR_PUB_RELAY) # npub1relay9mayry...
nc.single_relay_event()
nc.message_pool_events()

meta_data = nc.last_event_msg.content
data = json.loads(meta_data)

for meta in meta_struct:
    try:
        print(meta + ":",data[meta])
    except:
        print(meta,"?")
```
```
name: relay9may
username: relay9may
displayName: relay_info
about: ⚡ Relays (NIP-11 info)
picture: https://www..../wp-content/2023/04/relay9may-300x297.png
banner: https://nostr.build/i/3e58affb1c5...bc0cf2a20390a0a05.jpg
website: 
lud16: glassfairies51@walletofsatoshi.com
lud06: 
nip05: 
```

## links

main lib.

https://github.com/holgern/pynostr

inspiration

https://github.com/monty888/monstr

https://codeberg.org/mat/nostrfiles

---

Agora_Zero: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj

