"""
basic tools for agama_nost client

"""

WIDTH = 39


def print_head(label="head"):
    print()
    print("-"*WIDTH)
    print("-"*5, label)
    print("-"*WIDTH)


def short_str(s,l=10): 
    try:
        if len(s)>l*2+12: # 32+
            return str(s[:l])+"..."+str(s[-l:])
        else:
            return s
    except:
        return s
    

def new_key_generate(print_out=True):
        from pynostr.key import PrivateKey
        private_key = PrivateKey()
        public_key = private_key.public_key
        if print_out:
            print("[tools] New keys generate") 
            #self.print_keys_info()
        return public_key.bech32(), private_key


def get_relay_information(url: str, timeout: float = 2, add_url: bool = True):
    # NIP-11 // 'pynostr'
    import requests 
    headers = {'Accept': 'application/nostr+json', 'User-Agent': 'agama_nostr'}
    if "wss" in url:
        metadata_uri = url.replace("wss", "https")
    elif "ws" in url:
        metadata_uri = url.replace("ws", "http")
    else:
        raise Exception(f"{url} is not a websocket url")
    try:
        response = requests.get(metadata_uri, headers=headers, timeout=timeout)

        response.raise_for_status()

        metadata = response.json()
        if add_url:
            metadata["url"] = url
        return metadata
    except requests.exceptions.Timeout:
        # Handle a timeout error
        print("Request timed out. Please try again later.")

    except requests.exceptions.HTTPError as err:
        # Handle an HTTP error
        print(f"HTTP error occurred: {err}")

    except requests.exceptions.RequestException as err:
        # Handle any other request exception
        print(f"An error occurred: {err}")