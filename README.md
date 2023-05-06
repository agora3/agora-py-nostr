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
python3 -m venv venv  
source venv/bin/activate
pip install -r requirements.txt
// pip install pynostr 
export PYTHONPATH="$PYTHONPATH:./"


```

Basic usage (example)

```
from agama_nostr.client import Client 
from agama_nostr.nostr_key import NOSTR_SEC

nostr_client = Client(NOSTR_SEC)
# nostr_client.subscription(limit_num=20) 

...
```

Agora_Zero: npub1ag0ra0shs0sd24wqwqdceu2yzj3uj5xa53ge2vstz0nyf49ez68qqq2jgj

