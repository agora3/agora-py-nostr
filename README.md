# agora-py-nostr

simple Python Nostr Client

This is experimental software in early development


## Install

```
git clone https://github.com/agora3/agora-py-nostr.git
cd agora-py-nostr
//
python3 -m venv venv  
source venv/bin/activate
pip install -r requirements.txt
// pip install pynostr 
cp agama_nostr/nostr_key.py.tmp agama_nostr/nostr_key.py
export PYTHONPATH="$PYTHONPATH:./"
python nostr_key_gen.py 

// or sh:
chmod +x initial_setup.sh
./initial_setup.sh
```


## First start

```
setup your secret key in the file ./agama_nostr/nostr_key.py

NOSTR_SEC = "------ YOUR SECRET KEY -------"

or create new one:

$ python3 nostr_key_gen.py

---------------------------------------
----- new_key_generate
---------------------------------------
new pub.key: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj
NOSTR_SEC => 98b7b......................................................7a1f5

(you can save the NOSTR_SEC key in the file: ./agama_nostr/nostr_key.py)
``` 
 
## Basic usage (publish vevent)

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

## links

main lib.

https://github.com/holgern/pynostr

inspiration

https://github.com/monty888/monstr

https://codeberg.org/mat/nostrfiles

---

Agora_Zero: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj

