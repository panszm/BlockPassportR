from p2p.peer import Peer, PeerInfo
from bchain.node_types.node_type import NodeType
from bchain.chain import Chain
import pickle
import bchain.block
from bchain.transactions import *
from bchain.node_types.command_handler import CommandHandler
from time import sleep

class Node:

    def __init__(self, peer_info:PeerInfo, node_id):
        self.chain = Chain()
        self.handler = CommandHandler(self)
        self.peer = Peer(peer_info,command_handler=self.handler)
        self.peer.start_listening()
        self.node_id = node_id
    
    def make_connection(self, peer_info: PeerInfo):
        self.peer.make_connection(peer_info)
        self.send_command(11,len(self.chain.blocks))

    def initialize(self):
        self.peer.start_listening()

    def shutdown(self):
        self.save_bchain()
        self.peer.stop()

    def save_bchain(self, filepath="./data/bchain_data"):
        file = open(filepath, 'wb+')
        pickle.dump(self.chain, file)
        file.close()

    def load_bchain(self, filepath="./data/bchain_data"):
        file = open(filepath, 'rb')
        self.chain = pickle.load(file)
        file.close()

    def send_command(self, command_code, obj):
        self.peer.broadcast_command(command_code,obj)

    def c_new_block(self, block:bchain.block.Block):
        self.chain.add_block(block)

    def c_new_transaction(self, transaction:Transaction):
        if not self.chain.is_in_chain(transaction):
        #     self.chain.register_transaction(transaction)
            self.append_received_transaction(transaction)

    def c_chain_length_received(self, length, peer_info):
        if length > len(self.chain.blocks):
            self.peer.send_command(12, self.peer.get_info(), peer_info)
        elif length < len(self.chain.blocks):
            self.peer.send_command(11, len(self.chain.blocks))

    def c_chain_requested(self,peer_info):
        self.peer.send_command(13,self.chain,peer_info)

    def c_chain_received(self,chain:Chain):
        if chain.verify_chain and len(chain.blocks)>len(self.chain.blocks):
            self.chain = chain

    def append_transaction(self,transaction:Transaction):
        if self.chain.blocks[-1].is_full():
            self.chain.add_new_block()
            print("Adding new block")
            return False
        else:
            self.chain.register_transaction(transaction)
            return True

    def append_received_transaction(self,transaction:Transaction):
        while self.chain.blocks[-1].is_full():
            pass
        self.chain.register_transaction(transaction)


class GovernmentNode(Node):

    def create_passport(self,passport_id, date_from, date_to, country):
        new_passport = Transaction('p',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # if self.append_transaction(new_passport):
        #     self.peer.broadcast_command(31,new_passport)
        # else:
        #     self.peer.broadcast_command(21,self.chain.blocks[-1])
        if not self.append_transaction(new_passport):
            self.peer.broadcast_command(21,self.chain.blocks[-1])
            self.chain.register_transaction(new_passport)
        self.peer.broadcast_command(31,new_passport)

    def edit_passport(self,passport_id, date_from, date_to, country):
        edited_passport = Transaction('r',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # if self.append_transaction(edited_passport):
        #     self.peer.broadcast_command(32,edited_passport)
        # else:
        #     self.peer.broadcast_command(21,self.chain.blocks[-1])
        if not self.append_transaction(edited_passport):
            self.peer.broadcast_command(21,self.chain.blocks[-1])
            self.chain.register_transaction(edited_passport)
        self.peer.broadcast_command(31,edited_passport)

    def create_visa(self,passport_id, date_from, date_to, country):
        new_visa = Transaction('v',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # if self.append_transaction(new_visa):
        #     self.peer.broadcast_command(51,new_visa)
        # else:
        #     self.peer.broadcast_command(21,self.chain.blocks[-1])
        if not self.append_transaction(new_visa):
            self.peer.broadcast_command(21,self.chain.blocks[-1])
            self.chain.register_transaction(new_visa)
        self.peer.broadcast_command(31,new_visa)

class BorderControlNode(Node):

    def register_border_crossing(self,passport_id, date_from, date_to, country):
        border_crossing = Transaction('b',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # if self.append_transaction(border_crossing):
        #     self.peer.broadcast_command(41, border_crossing)
        # else:
        #     self.peer.broadcast_command(21,self.chain.blocks[-1])
        if not self.append_transaction(border_crossing):
            self.peer.broadcast_command(21,self.chain.blocks[-1])
            self.chain.register_transaction(border_crossing)
        self.peer.broadcast_command(31,border_crossing)

class EnforcementNode(Node):

    pass

class APINode(Node):

    pass