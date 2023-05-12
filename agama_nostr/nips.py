"""
nips
https://github.com/nostr-protocol/nips
"""

nip_11_struct = [ "name","description","pubkey","contact","supported_nips","software","version"]
nip_11_struct_adv = [ "name","description","pubkey","contact","supported_nips","software","version","limitation"]

"""
NIP-11
 "name": <string identifying relay>,
 "description": <string with detailed information>,
 "pubkey": <administrative contact pubkey>,
 "contact": <administrative alternate contact>,
 "supported_nips": <a list of NIP numbers supported by the relay>,
 "software": <string identifying relay software URL>,
 "version": <string version identifier>
"""

meta_struct = ["name","username","displayName","about","picture","banner","website","lud16","lud06","nip05"]

"""
NIP-05: Mapping Nostr keys to DNS-based internet identifiers

meta_info

{"display_name":"relay_info",
 "name":"relay9may",
 "username":"relay9may",
 "displayName":"relay_info",
 "about":"relays info",
 "lud16":"...*@walletofsatoshi.com",
 "picture":"https://.../relay9may-300x297.png",
 "banner":"https://nostr.build/i/3e58af31b3f68fb1c5bef12de3c29d8f604f13460bc0cf40fa0b2a20390a0a05.jpg",
 "website":"",
 "nip05":"",
 "lud06":""}
"""