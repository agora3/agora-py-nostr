# agora-py-nostr

main lib.

https://github.com/holgern/pynostr

inspiration

https://github.com/monty888/monstr

https://codeberg.org/mat/nostrfiles


---

Install

```
git clone https://github.com/agora3/agora-py-nostr.git
cd agora-py-nostr
//--- sh:
chmod +x initial_setup.sh
./initial_setup.sh


//---- or:
python3 -m venv venv  
source venv/bin/activate
pip install -r requirements.txt
// pip install pynostr 

export PYTHONPATH="$PYTHONPATH:./"
cp agama_nostr/nostr_key.py.tmp agama_nostr/nostr_key.py
python nostr_key_gen.py 

```

Basic usage (example)

```
setup your secret key in the file ./agama_nostr/nostr_key.py

NOSTR_SEC = "------ YOUR SECRET KEY -------"

or create new one:

$ python test/nostr_key_gen.py

---------------------------------------
----- new_key_generate
---------------------------------------
new pub.key: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj
NOSTR_SEC => 98b7b......................................................7a1f4

(you can save the NOSTR_SEC key in the file: ./agama_nostr/nostr_key.py)
 



your project:

from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC

nostr_client = Client(NOSTR_SEC)
# nostr_client.subscription(limit_num=20) 

...
```

Agora_Zero: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj

