#!/usr/bin/env python

"""
https://github.com/agora3/agora-py-nostr
# filters: EventKind.TEXT_NOTE / SET_METADATA / RECOMMEND_RELAY / CONTACTS / ENCRYPTED_DIRECT_MESSAGE / DELETE
# self.relay_manager.publish_event / publish_message

usage:

nc = Client(NOSTR_SEC) # nostr_client

"""

from time import sleep, monotonic
from rich.console import Console
from rich.table import Table
import json, ssl, uuid
from pynostr.relay_manager import RelayManager
from pynostr.filters import FiltersList, Filters
from pynostr.key import PrivateKey, PublicKey
from pynostr.relay import Relay
from pynostr.event import Event, EventKind 
from pynostr.base_relay import RelayPolicy
from pynostr.relay_list import RelayList
from pynostr.message_pool import MessagePool
from pynostr.message_type import RelayMessageType, ClientMessageType
from pynostr.metadata import Metadata
from pynostr.utils import get_public_key, get_relay_list, get_timestamp
from pynostr.encrypted_dm import EncryptedDirectMessage
import tornado.ioloop
from tornado import gen
from agama_nostr.relays import relays_list
from agama_nostr.tools import get_relay_information

__version__ = "0.2.8" # 2023/05/12


DEBUG = True
RELAY_URL = "wss://relay.damus.io" # relays_list[0] # single main relay "wss://relay.damus.io"
nip_11_struct_select = ["name","description","software"]

console = Console()


class Client():
    def __init__(self, nostr_sec=None, relays=True):
        try:
            self.private_key = PrivateKey.from_hex(nostr_sec)
            self.public_key = self.private_key.public_key
        except:
            print("Err. private_key")
            self.private_key = None
            self.public_key = None
        if DEBUG:
            print("[Client init]")
            self.print_keys_info()

        if relays:    
            self.connect_to_relay()
        

        self.message_pool = MessagePool(first_response_only=False)
        self.last_event_msg = None
        self.policy = RelayPolicy()
        self.set_subscription_id()
        self.io_loop = tornado.ioloop.IOLoop.current()
        self.contacts = None
        self.contacts_event = None
        self.contacts_for_relay = {}
        self.contact_timeout = 0
        self.contacts_last = -1
        

    def print_keys_info(self):
        try:
            print(f"Private key: {self.private_key.bech32()}")
            print("=>", self.private_key)
            print(f"Public key:  {self.public_key.bech32()}")
        except:
            print("Err. print_keys_info")


    def new_key_generate(self, print_out=True):
        self.private_key = PrivateKey()
        self.public_key = self.private_key.public_key
        if print_out:
            print("[New keys generate]") 
            self.print_keys_info()
        return self.public_key.bech32(), self.private_key


    def print_myrelays_list(self):
        for relay in relays_list:
            print(relay)
        print()


    def connect_to_relay(self,timeout=5):
        if DEBUG:  print("[Relay manager] connect_to_relays")
        self.relay_manager = RelayManager(timeout=timeout)
                        
        for relay in relays_list:
            self.relay_manager.add_relay(relay)
            if DEBUG:
                print("-"*39)  
                print("[add_relay]", relay) 
                sleep(0.3)

                relay_data = get_relay_information(relay)
                try:
                    for info in nip_11_struct_select:
                        print("{:<13s} - {}".format(info,str(relay_data.get(info))))
                except:
                    print("Err. parse relay_data")

 
    def single_relay_init(self, relay="R", timeout=5):
        if relay == "R": relay = RELAY_URL
        self.r = Relay(relay, self.message_pool, self.io_loop, self.policy, timeout=timeout)
        self.r.add_subscription(self.subscription_id, self.filters)


    def close_connections(self):
        if DEBUG: print("[class DEBUG] relay_manager.close_connections")
        self.relay_manager.close_connections()
        #self.io_loop.remove_timeout
        #self.io_loop.close()


    def scann_relay_list(self):
        relay_list = RelayList()
        relay_list.append_url_list(get_relay_list())

        print(f"Checking {len(relay_list.data)} relays...") # [2023/03] Checking 282 relays...

        relay_list.update_relay_information(timeout=0.5)
        relay_list.drop_empty_metadata()

        print(f"Found {len(relay_list.data)} relays and start searching for metadata...") # Found 236 relays and start searching for metadata...


    def set_subscription_id(self,sub_str_hex=""):
        if sub_str_hex == "":
            self.subscription_id = uuid.uuid1().hex
            #self.prof_sub = uuid.uuid4().hex
        else:
            self.subscription_id = sub_str_hex
        if DEBUG: print("set_subscription_id",self.subscription_id)


    def parse_author(self,nostr_user=""):
        if nostr_user == "":
            author = self.private_key.public_key.hex()
        else:
            author = PublicKey.from_npub(nostr_user).hex()
        return author


    def set_filter_meta(self, nostr_user=""):
        author = self.parse_author(nostr_user)          
        self.filters = FiltersList([Filters(authors=[author],kinds=[EventKind.SET_METADATA])])
        if DEBUG: print("[class DEBUG] set_filters",str(self.filters))


    def set_filter_contact(self, nostr_user=""):
        author = self.parse_author(nostr_user)
        self.filters = FiltersList([Filters(authors=[author],kinds=[EventKind.CONTACTS])])
        self.contact_timeout = monotonic() + 10
        if DEBUG: print("[class DEBUG] set_filters",str(self.filters))


    def get_contacts(self):
        if DEBUG: print("[class DEBUG] getting existing contacts")
        while monotonic() < self.contact_timeout:
            if self.relay_manager.message_pool.has_events():
                event_msg = self.relay_manager.message_pool.get_event()
                print("ev_msg",event_msg)
                if event_msg.event.kind == EventKind.CONTACTS:
                    if DEBUG: print("got %d contacts from %s", len(event_msg.event.tags), event_msg.url)
                    self.contacts_for_relay[event_msg.url] = event_msg.event.tags
                    if event_msg.event.created_at > self.contacts_last:
                        self.contacts = event_msg.event.tags
                        self.contacts_event = event_msg.event
                        self.contacts_last = event_msg.event.created_at
            if not self.relay_manager.message_pool.has_events(): # 'Client' object has no attribute 'contacts_event'
                sleep(0.25)
        if DEBUG: print("[class DEBUG] done getting existing contacts")
        return self.contacts_event


    def set_filters(self, since=0,nostr_user="",limit_num=10):
        if since > 0:
            self.filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()],kinds=[EventKind.TEXT_NOTE], since=since,limit=limit_num)])
        else:
            self.filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])

        if nostr_user =="":
            print() # test        
        else:
            author = self.parse_author(nostr_user)
            self.filters = FiltersList([Filters(authors=[author],kinds=[EventKind.TEXT_NOTE],limit=limit_num)])
        
        """
        self.filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        if since>0:
            self.filters = FiltersList.append([Filters(since=since)])
        """        
        if DEBUG: print("[class DEBUG] set_filters",str(self.filters))


    def publish_event(self, txt="Hello Nostr", relay=""):
        # simple_event expand
        event = Event(content=txt,)
        event.sign(self.private_key.hex())
            
        if DEBUG: print("[class DEBUG] publish_event",txt,event)

        if relay == "": # from users-list of relays
            self.relay_manager.publish_event(event)
            self.relay_manager.run_sync()
            sleep(3) # allow the messages to send

            while self.relay_manager.message_pool.has_ok_notices():
                ok_msg = self.relay_manager.message_pool.get_ok_notice()
                if DEBUG: print("[class DEBUG] message_pool.get_ok_notice: ",ok_msg)
                sleep(1)

        else: # single specific relay
            self.single_relay_init(relay=relay, timeout=5)    
            self.r.publish(event.to_message())
            try:
                self.io_loop.run_sync(self.r.connect) # multi: asyncio.exceptions.TimeoutError: Operation timed out after None seconds
            except gen.Return:
                pass
            self.io_loop.stop()


    def single_relay_event(self):
        self.single_relay_init()      
        # x-self.r.publish(event.to_message())
        try:
            self.io_loop.run_sync(self.r.connect) # multi: asyncio.exceptions.TimeoutError: Operation timed out after None seconds
        except gen.Return:
            pass
        self.io_loop.stop()


    def message_pool_events(self):
        index = 0
        if DEBUG:
            print("-"*39) 
            print("[class DEBUG] message_pool_events")
        while self.message_pool.has_events():
            if DEBUG: print("-"*12,"has_events [index]",index)
            event_msg = self.message_pool.get_event()
            print(event_msg.event.content)
            index += 1
        #self.last_event_msg = event_msg.event.content
        try:
            self.last_event_msg = event_msg.event
            return event_msg.event.content
        except:
            return "?"


    def message_pool_notices(self):
        index = 0
        if DEBUG:
            print("-"*39) 
            print("[class DEBUG] message_pool_notices")
        while self.message_pool.has_notices():
            if DEBUG: print("-"*12,"has_notices [index]",index)
            notice_msg = self.message_pool.get_notice()
            print(notice_msg.content)
            index += 1
        

    # publish_note / thread
    def replay_event(self, original_note_id, original_note_author_pubkey, txt="Reply"):
        reply = Event(content=txt,)
        # create 'e' tag reference to the note you're replying to
        reply.add_event_ref(original_note_id)
        # create 'p' tag reference to the pubkey you're replying to
        reply.add_pubkey_ref(original_note_author_pubkey)
        reply.sign(self.private_key.hex())

        self.relay_manager.publish_event(reply)
        self.relay_manager.run_sync()
        sleep(3) # allow the messages to send
        #self.relay_manager.close_connections()

        while self.relay_manager.message_pool.has_ok_notices():
            ok_msg = self.relay_manager.message_pool.get_ok_notice()
            print("ok_msg",ok_msg)
            sleep(1)


    def receive_event(self):
        ##self.filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()], kinds=[EventKind.TEXT_NOTE])])
        request = [ClientMessageType.REQUEST, self.subscription_id]
        request.extend(self.filters.to_json_array())

        self.relay_manager.add_subscription_on_all_relays(self.subscription_id, self.filters)
        self.relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE})  # NOTE: This disables ssl certificate verification
        sleep(1.25)  # allow the connections to open

        message = json.dumps(request)
        self.relay_manager.publish_message(message)
        sleep(1.5)  # allow the messages to send

        while self.relay_manager.message_pool.has_events():
            event_msg = self.relay_manager.message_pool.get_event()
            print(event_msg.event.content)

        self.relay_manager.close_connections()

    
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


    def send_direct_message(self, recipient_str, msg, relay=""):
        if DEBUG: print("[class DEBUG] send_direct_message")
        self.sender_pk = self.private_key #sender_pk = PrivateKey.from_hex(NOSTR_SEC)
        self.recipient = get_public_key(recipient_str) #public_key = sender_pk.public_key 
        if DEBUG:
            if self.recipient != "":
                print(f"[class DEBUG] recipient is set to {self.recipient.bech32()}")
            else:
                raise Exception("reciever not valid")

        self.filters = FiltersList([Filters(authors=[self.recipient.hex()], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],since=get_timestamp(),limit=1,)])
        
        dm = EncryptedDirectMessage()
        dm.encrypt( self.sender_pk.hex(), cleartext_content=msg, recipient_pubkey=self.recipient.hex(), )
        dm_event = dm.to_event()
        dm_event.sign(self.sender_pk.hex())   

        if relay == "":
            if DEBUG: print("[class DEBUG] list of relays")
            #self.relay_manager.publish_event(dm_event.to_message())
            self.relay_manager.publish_event(dm_event)
            self.relay_manager.run_sync()
            sleep(3) # allow the messages to send

            while self.relay_manager.message_pool.has_ok_notices():
                ok_msg = self.relay_manager.message_pool.get_ok_notice()
                if DEBUG: print("[class DEBUG] message_pool.get_ok_notice: ",ok_msg)
                sleep(1)
        else:
            if DEBUG: print("[class DEBUG] single relay", relay) # only for testing
            if relay == "R": relay = RELAY_URL
            self.r = Relay(relay, self.message_pool, self.io_loop, self.policy, timeout=5, close_on_eose=False, message_callback=self.print_dm, )
            
            self.r.publish(dm_event.to_message())
            self.r.add_subscription(self.subscription_id, self.filters)
            
            # temp. modifik - ToDo better
            self.io_loop_run()


    def list_events_old(self):
        self.single_relay_init()
        self.io_loop_run()
        self.get_all_events_table()


    def get_all_events_data(self):
        event_msgs = self.message_pool.get_all_events()
        if DEBUG: print(f"{self.r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")

        evs = []
        for event_msg in event_msgs[::-1]:
            evs.append(str(event_msg.event.date_time()) + "\n" + str(event_msg.event.content))
        return evs
        

    def get_all_events_table(self):
        event_msgs = self.message_pool.get_all_events()
        print(f"{self.r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")
        
        table = Table("date", "content")
        for event_msg in event_msgs[::-1]:
            table.add_row(str(event_msg.event.date_time()), event_msg.event.content)
        console.print(table)
        return event_msgs


    def list_events(self):  
        #r = Relay(relay_url, message_pool, io_loop, policy, timeout=5, close_on_eose=False, message_callback=print_dm, )
        #filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        #self.set_filters(limit_num)
        self.relay_manager.add_subscription_on_all_relays(self.subscription_id, self.filters)
        #io_loop_run()
        
        event_msgs = self.message_pool.get_all_events()
        ##print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")
        print(f"x returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")

        table = Table("date", "content")
        for event_msg in event_msgs[::-1]:
            table.add_row(str(event_msg.event.date_time()), event_msg.event.content)
        console.print(table)


    def io_loop_run(self):
        if DEBUG: print("[class DEBUG] io_loop")
        try:            
            self.io_loop.run_sync(self.r.connect)
            #sleep(2)
            #self.io_loop.stop()
        except gen.Return:
            pass
        if DEBUG: print("io_loop.stop")
        self.io_loop.stop()
