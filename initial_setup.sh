echo "-------------------------"
echo "agama lib. | agora nostr "
echo "-------------------------" 

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export PYTHONPATH="$PYTHONPATH:./"

echo "--- rename ------------------"
echo "agama_nostr/nostr_key.py.tmp "
cp ./agama_nostr/nostr_key.py.tmp ./agama_nostr/nostr_key.py

echo
python nostr_key_gen.py

