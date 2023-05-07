#!/bin/sh

echo "-------------------------"
echo "agama lib. | agora nostr "
echo "-------------------------" 

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export PYTHONPATH="$PYTHONPATH:./"


# protection against accidental overwriting of an existing file
if [! -f "./agama_nostr/nostr_key.py"]; then
    echo "--- rename ------------------"
    echo "agama_nostr/nostr_key.py.tmp "
    cp ./agama_nostr/nostr_key.py.tmp ./agama_nostr/nostr_key.py
    echo "-> agama_nostr/nostr_key.py"
fi

echo

# automatic generation of a random key that can be used
python nostr_key_gen.py
