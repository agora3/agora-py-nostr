#!/bin/sh
echo "-------------------------"
echo "agama lib. | agora nostr "
echo "-------------------------" 

virtualenv -p python3.8 venv
. venv/bin/activate
pip install -r requirements.txt

# automatic generation of a random key that can be used
export PYTHONPATH="$PYTHONPATH:./"
python nostr_key_gen.py
