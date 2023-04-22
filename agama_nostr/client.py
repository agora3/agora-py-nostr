"""
https://github.com/agora3/agora-py-nostr
"""
from time import sleep
from rich.console import Console
from rich.table import Table
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
from pynostr.message_type import RelayMessageType
from pynostr.metadata import Metadata
from pynostr.relay_list import RelayList
from pynostr.utils import get_public_key, get_relay_list, get_timestamp
from pynostr.encrypted_dm import EncryptedDirectMessage

import tornado.ioloop
from tornado import gen


DEBUG = True
RELAY_URL = "wss://relay.damus.io"


console = Console()
"""
input_str = input("author (npub or nip05): ")
recipient = ""
author = get_public_key(input_str)

"""

"""
@gen.coroutine
def print_dm(message_json):
    if DEBUG: print("[print_dm()]", message_json)
"""


class Client():
    def __init__(self, nostr_sec):
        self.private_key = PrivateKey.from_hex(nostr_sec)
        self.public_key = self.private_key.public_key
        if DEBUG:
            print("[Client init]")
            self.print_keys_info()
            
        self.connect_to_relay()
          

    def print_keys_info(self):
        print(f"Private key: {self.private_key.bech32()}")
        print("=>", self.private_key)
        print(f"Public key:  {self.public_key.bech32()}")


    def new_key_generate(self):
        self.private_key = PrivateKey()
        self.public_key = self.private_key.public_key
        if DEBUG:
            print("[New keys generate]") 
            self.print_keys_info()


    def connect_to_relay(self):
        if DEBUG:  print("[Relay manager]")
        self.relay_manager = RelayManager(timeout=6)
        if DEBUG:  print("add_relay", RELAY_URL) # ToDo extern array of relays
        self.relay_manager.add_relay(RELAY_URL)
        """
        self.relay_manager.add_relay("wss://nostr.mnethome.de")
        self.relay_manager.add_relay("wss://relay.damus.io")
        self.relay_manager.add_relay("wss://nostr-pub.wellorder.net")
        self.relay_manager.add_relay("wss://relay.nostr.ch")
        self.relay_manager.add_relay("wss://nostr.onsats.org")
        self.relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})  # CERT_NONE disables ssl certificate verification
        sleep(1)
        """


    def set_subscription_id(self):
        self.subscription_id = uuid.uuid1().hex
        if DEBUG: print("set_subscription_id",self.subscription_id)


    def subscription(self, limit_num = 10):
        self.set_subscription_id()
        filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()], limit=limit_num)])
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


    def scann_relay_list(self):
        relay_list = RelayList()
        relay_list.append_url_list(get_relay_list())

        print(f"Checking {len(relay_list.data)} relays...") # [2023/03] Checking 282 relays...

        relay_list.update_relay_information(timeout=0.5)
        relay_list.drop_empty_metadata()

        print(f"Found {len(relay_list.data)} relays and start searching for metadata...") # Found 236 relays and start searching for metadata...

    
    @gen.coroutine
    def print_dm(self, message_json):
        if DEBUG: print("[print_dm()]", message_json)
        message_type = message_json[0]
        if message_type == RelayMessageType.EVENT:
            event = Event.from_dict(message_json[2])
            if event.kind == EventKind.ENCRYPTED_DIRECT_MESSAGE:
                if event.has_pubkey_ref(self.sender_pk.public_key.hex()):
                    rdm = EncryptedDirectMessage.from_event(event)
                    rdm.decrypt(self.sender_pk.hex(), public_key_hex=self.recipient.hex())
                    print(f"New dm received:{event.date_time()} {rdm.cleartext_content}")
        elif message_type == RelayMessageType.OK:
            print(message_json)
        elif message_type == RelayMessageType.NOTICE:
            print(message_json)


    def send_mess(self, recipient_str, msg):
        #sender_pk = PrivateKey.from_hex(NOSTR_SEC)
        self.sender_pk = self.private_key
        #public_key = sender_pk.public_key 
        #recipient_str = input("recipient (npub or nip05): ")
        self.recipient = get_public_key(recipient_str)
        if DEBUG:
            if self.recipient != "":
                print(f"recipient is set to {self.recipient.bech32()}")
            else:
                raise Exception("reciever not valid")

        #msg = input("message: ")
        #relay_url = RELAY_URL # input("relay: ")

        dm = EncryptedDirectMessage()
        dm.encrypt( self.sender_pk.hex(), cleartext_content=msg, recipient_pubkey=self.recipient.hex(), )

        filters = FiltersList(
            [
            Filters(authors=[self.recipient.hex()], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],since=get_timestamp(),limit=1, )
            ]
        ) # old-ok: limit=10

        subscription_id = uuid.uuid1().hex
        io_loop = tornado.ioloop.IOLoop.current()
        message_pool = MessagePool(first_response_only=False)
        policy = RelayPolicy()

        r = Relay(RELAY_URL, message_pool, io_loop, policy, timeout=5, close_on_eose=False, message_callback=self.print_dm, )
        dm_event = dm.to_event()
        dm_event.sign(self.sender_pk.hex())
        
        r.publish(dm_event.to_message())
        r.add_subscription(subscription_id, filters)
        
        # temp. modifik - ToDo better
        if DEBUG: print("[io_loop]")
        try:            
            io_loop.run_sync(r.connect)
            sleep(5)
            io_loop.stop()
        except gen.Return:
            pass
        if DEBUG: print("[io_loop] stop")
        # io_loop.stop()


    def list_events(self,limit_num = 10):
        self.set_subscription_id()
        message_pool = MessagePool(first_response_only=False)
        policy = RelayPolicy()
        io_loop = tornado.ioloop.IOLoop.current()
        r  = Relay(RELAY_URL, message_pool, io_loop, policy, timeout=2)
        #r = Relay(relay_url, message_pool, io_loop, policy, timeout=5, close_on_eose=False, message_callback=print_dm, )
        filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        r.add_subscription(self.subscription_id, filters)

        try:
            io_loop.run_sync(r.connect)
        except gen.Return:
            pass
        io_loop.stop()
        
        event_msgs = message_pool.get_all_events()
        print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")

        table = Table("date", "content")
        for event_msg in event_msgs[::-1]:
            table.add_row(str(event_msg.event.date_time()), event_msg.event.content)
        console.print(table)


        """    
        index = 0
        while message_pool.has_notices():
            if DEBUG: print("-"*20, "has_notices [index]", index)
            notice_msg = message_pool.get_notice()
            print(notice_msg.content)
            index += 1

        index = 0    
        while message_pool.has_events():
            if DEBUG: print("-"*20, "has_events [index]", index)
            event_msg = message_pool.get_event()
            print(event_msg.event.content)
            index += 1
        """