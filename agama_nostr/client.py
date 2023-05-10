"""
https://github.com/agora3/agora-py-nostr
"""
from time import sleep
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

__version__ = "0.2.5"


DEBUG = True
RELAY_URL = relays_list[0] # single main relay "wss://relay.damus.io"
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
        self.policy = RelayPolicy()
        self.set_subscription_id()
        self.io_loop = tornado.ioloop.IOLoop.current()
        

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
        else:
            self.subscription_id = sub_str_hex
        if DEBUG: print("set_subscription_id",self.subscription_id)


    def set_filter_meta(self, nostr_user=""):
        if nostr_user == "":
            author = self.private_key.public_key.hex()            
        else:
            author = PublicKey.from_npub(nostr_user).hex()
          
        self.filters = FiltersList([Filters(authors=[author],kinds=[EventKind.SET_METADATA])])
        if DEBUG:
            print("[class DEBUG] set_filters",str(self.filters))
            print("- nostr_user_hex",author)
        

    def set_filters(self, since=0,limit_num=10):
        """
        NIP-01 filtering. Explicitly supports "#e" and "#p" tag filters via `event_refs`
        and `pubkey_refs`. Arbitrary NIP-12 single-letter tag filters are also supported via
        `add_arbitrary_tag`. If a particular single-letter tag gains prominence, explicit
        support should be added. For example:
        
        # arbitrary tag
        filter.add_arbitrary_tag('t', [hashtags])

        # promoted to explicit support
        Filters(hashtag_refs=[hashtags])
        :param ids: List[str]
        :param kinds: List[EventKind]
        :param authors: List[str]
        :param since: int
        :param until: int
        :param event_refs: List[str]
        :param pubkey_refs: List[str]
        :param limit: int

        # EventKind.SET_METADATA, EventKind.RECOMMEND_RELAY, EventKind.CONTACTS, EventKind.ENCRYPTED_DIRECT_MESSAGE, EventKind.DELETE])])
        """
        #self.filters= FiltersList([Filters(authors=[self.private_key.public_key.hex()], kinds=[EventKind.TEXT_NOTE])])
        if since > 0:
            self.filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()],kinds=[EventKind.TEXT_NOTE], since=since,limit=limit_num)])
        else:
            self.filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        """
        self.filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        if since>0:
            self.filters = FiltersList.append([Filters(since=since)])
        """        
        if DEBUG:
            print("[class DEBUG] set_filters",str(self.filters))


    #def subscription(self, limit_num = 10):
    #    self.set_subscription_id()
    #    self.filters = FiltersList([Filters(authors=[self.private_key.public_key.hex()], limit=limit_num)])
    #    self.relay_manager.add_subscription_on_all_relays(self.subscription_id, self.filters)
 

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
            if relay == "R": relay = RELAY_URL
            r = Relay(relay, self.message_pool, self.io_loop, self.policy, timeout=5)
            r.add_subscription(self.subscription_id, self.filters)
       
            r.publish(event.to_message())
            try:
                self.io_loop.run_sync(r.connect) # multi: asyncio.exceptions.TimeoutError: Operation timed out after None seconds
            except gen.Return:
                pass
            self.io_loop.stop()


    def single_relay_event(self):        
        r = Relay(RELAY_URL, self.message_pool, self.io_loop, self.policy, timeout=5)
        r.add_subscription(self.subscription_id, self.filters)

        try:
            self.io_loop.run_sync(r.connect) # multi: asyncio.exceptions.TimeoutError: Operation timed out after None seconds
        except gen.Return:
            pass
        self.io_loop.stop()

        """
        index = 0
        if DEBUG: print("[events]")    
        while self.message_pool.has_events():
            if DEBUG: print("has_events [index]", index)
            event_msg = self.message_pool.get_event()
            print(event_msg.event.content)
            index += 1
        """


    # publish_note / thread
    def replay_event(self, original_note_id, original_note_author_pubkey, txt="Reply: Hello Nostr"):
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
        # EventKind.SET_METADATA, EventKind.RECOMMEND_RELAY, EventKind.CONTACTS, EventKind.ENCRYPTED_DIRECT_MESSAGE, EventKind.DELETE])])
        ##self.subscription_id = "my-python-event"
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

    """
    def nostr_send_dm(self, msg:str):
        dm = EncryptedDirectMessage(
            recipient_pubkey=self.private_key.public_key.hex(),
            cleartext_content=msg)
        self.private_key.sign_event(dm)
        self.relay_manager.publish_event(dm)
    """


    def send_direct_message(self, recipient_str, msg, relay=""):
        if DEBUG: print("[class DEBUG] send_direct_message")
        self.sender_pk = self.private_key #sender_pk = PrivateKey.from_hex(NOSTR_SEC)
        self.recipient = get_public_key(recipient_str) #public_key = sender_pk.public_key 
        if DEBUG:
            if self.recipient != "":
                print(f"[class DEBUG] recipient is set to {self.recipient.bech32()}")
            else:
                raise Exception("reciever not valid")

        ##self.set_subscription_id()
        self.filters = FiltersList([Filters(authors=[self.recipient.hex()], kinds=[EventKind.ENCRYPTED_DIRECT_MESSAGE],since=get_timestamp(),limit=1,)])
        
        dm = EncryptedDirectMessage()
        dm.encrypt( self.sender_pk.hex(), cleartext_content=msg, recipient_pubkey=self.recipient.hex(), )
        dm_event = dm.to_event()
        dm_event.sign(self.sender_pk.hex())        

        if relay == "":
            if DEBUG: print("[class DEBUG] list of relays")
        else:
            if DEBUG: print("[class DEBUG] single relay", relay)
            if relay == "R": relay = RELAY_URL
            r = Relay(relay, self.message_pool, self.io_loop, self.policy, timeout=5, close_on_eose=False, message_callback=self.print_dm, )
            
            r.publish(dm_event.to_message())
            r.add_subscription(self.subscription_id, self.filters)
            
            # temp. modifik - ToDo better
            if DEBUG: print("[class DEBUG] io_loop")
            try:            
                self.io_loop.run_sync(r.connect)
                sleep(5)
                self.io_loop.stop()
            except gen.Return:
                pass
            if DEBUG: print("io_loop.stop")
            # io_loop.stop()


    def list_events_old(self):
  
        r = Relay(RELAY_URL, self.message_pool, self.io_loop, self.policy, timeout=5)
        #r = Relay(relay_url, message_pool, io_loop, policy, timeout=5, close_on_eose=False, message_callback=print_dm, )
        
        r.add_subscription(self.subscription_id, self.filters)
        #self.relay_manager.add_subscription_on_all_relays(self.subscription_id, self.filters)

        try:
            self.io_loop.run_sync(r.connect)
            #self.relay_manager.run_sync()
        except gen.Return:
            pass
        self.io_loop.stop()
        
        event_msgs = self.message_pool.get_all_events()
        print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")
        #print(f"x returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")


        table = Table("date", "content")
        for event_msg in event_msgs[::-1]:
            table.add_row(str(event_msg.event.date_time()), event_msg.event.content)
        console.print(table)


    def list_events(self):  
        ##r  = Relay(RELAY_URL, message_pool, io_loop, policy, timeout=5)
        #r = Relay(relay_url, message_pool, io_loop, policy, timeout=5, close_on_eose=False, message_callback=print_dm, )

        #filters = FiltersList([Filters(kinds=[EventKind.TEXT_NOTE], limit=limit_num)])
        #self.set_filters(limit_num)
        
        ##r.add_subscription(self.subscription_id, self.filters)
        self.relay_manager.add_subscription_on_all_relays(self.subscription_id, self.filters)

        """
        try:
            ##io_loop.run_sync(r.connect)
            self.relay_manager.run_sync() # Err. Operation timed out after None seconds
        except gen.Return:
            pass
        ##io_loop.stop()
        """
        
        event_msgs = self.message_pool.get_all_events()
        ##print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")
        print(f"x returned {len(event_msgs)} TEXT_NOTEs from {self.public_key}.")

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