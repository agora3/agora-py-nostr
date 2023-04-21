
DEBUG = True

print("[1-key-gen] - test")
from pynostr.key import PrivateKey

private_key = PrivateKey()
public_key = private_key.public_key
print(f"Private key: {private_key.bech32()}")
print(f"Public key: {public_key.bech32()}")
"""
[1-key-gen]
Private key: nsec13rffw69.....set4lle
Public key: npub1fugww2pdkyn3kkqfrsa62d5j3r6y84wtzpmtqgtu4wk66stwkfjs3sm36g
...
Private key: nsec1curcsvt.....qfxlasx
Public key: npub1dpgzl38rtgakrdx53qpgnvqxzgam6zd6gk4s2xwphduf77rxk39q4ln68e
...

"""
RELAY_URL = "wss://relay.damus.io"
print("[2-connect-to-single-relay]", RELAY_URL)

from pynostr.relay import Relay
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
import tornado.ioloop
from tornado import gen
import time
import uuid


message_pool = MessagePool(first_response_only=False)
policy = RelayPolicy()
io_loop = tornado.ioloop.IOLoop.current()
r = Relay(RELAY_URL, message_pool, io_loop, policy, timeout=2)
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
subscription_id = uuid.uuid1().hex

r.add_subscription(subscription_id, filters)

try:
    io_loop.run_sync(r.connect)
except gen.Return:
    pass
io_loop.stop()

index = 0
while message_pool.has_notices():
    if DEBUG: print("has_notices [index]", index)
    notice_msg = message_pool.get_notice()
    print(notice_msg.content)
    index += 1

index = 0    
while message_pool.has_events():
    if DEBUG: print("has_events [index]", index)
    event_msg = message_pool.get_event()
    print(event_msg.event.content)
    index += 1




"""
print("[3-connect-to-relays]")
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.event import EventKind
import time
import uuid

relay_manager = RelayManager(timeout=2)
relay_manager.add_relay("wss://nostr-pub.wellorder.net")
relay_manager.add_relay("wss://relay.damus.io") # single
filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=100)])
subscription_id = uuid.uuid1().hex
relay_manager.add_subscription_on_all_relays(subscription_id, filters)
relay_manager.run_sync()
while relay_manager.message_pool.has_notices():
    notice_msg = relay_manager.message_pool.get_notice()
    print(notice_msg.content)
while relay_manager.message_pool.has_events():
    event_msg = relay_manager.message_pool.get_event()
    print(event_msg.event.content)
relay_manager.close_all_relay_connections()

"""


