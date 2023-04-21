# agora-py-nostr

main lib.

https://github.com/holgern/pynostr

---

Install

```
python3 -m venv venv  
source venv/bin/activate
// pip install -r requirements.txt
pip install pynostr 
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

