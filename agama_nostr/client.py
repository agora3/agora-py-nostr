import json
import ssl
import time
import uuid
# import codecs
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.key import PrivateKey
from pynostr.relay import Relay
from pynostr.event import Event, EventKind 
from pynostr.base_relay import RelayPolicy
from pynostr.message_pool import MessagePool
from pynostr.message_type import ClientMessageType
import tornado.ioloop
from tornado import gen


DEBUG = True
RELAY_URL = "wss://relay.damus.io"



class Client():
    def __init__(self, nostr_sec):
        self.private_key = PrivateKey.from_hex(nostr_sec)
        self.public_key = self.private_key.public_key
        if DEBUG:
            print("[Client init]")
            print(f"Private key: {self.private_key.bech32()}")
            print(f"Public key: {self.public_key.bech32()}")

        if DEBUG:  print("[Relay manager]")
        self.relay_manager = RelayManager(timeout=6)
        if DEBUG:  print("add_relay", RELAY_URL) # ToDo extern array of relays
        self.relay_manager.add_relay(RELAY_URL)


    def subscription(self, limit_num = 10):
        filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()], limit=limit_num)])
        
        self.subscription_id = uuid.uuid1().hex
        if DEBUG:  print("subscription_id", self.subscription_id)
        self.relay_manager.add_subscription_on_all_relays(self.subscription_id, filters)
 

    def simple_event(self, txt="Hello Nostr"):
        event = Event(txt)
        event.sign(self.private_key.hex())
        if DEBUG: print("publish", txt, event)
        self.relay_manager.publish_event(event)
        self.relay_manager.run_sync()
        time.sleep(5) # allow the messages to send

        while self.relay_manager.message_pool.has_ok_notices():
            ok_msg = self.relay_manager.message_pool.get_ok_notice()
            print("ok_msg",ok_msg)
            time.sleep(1)


    def list_events(self,limit_num = 10):
        message_pool = MessagePool(first_response_only=False)
        policy = RelayPolicy()
        io_loop = tornado.ioloop.IOLoop.current()
        r = Relay(RELAY_URL, message_pool, io_loop, policy, timeout=2)
        filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        self.subscription_id = uuid.uuid1().hex

        r.add_subscription(self.subscription_id, filters)

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
