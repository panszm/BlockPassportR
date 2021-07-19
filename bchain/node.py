from p2p.peer import Peer, PeerInfo
from bchain.node_types.node_type import NodeType
from bchain.chain import Chain
import pickle
import bchain.block
from bchain.transactions import *
from bchain.node_types.command_handler import CommandHandler

class Node:

    def __init__(self, peer_info:PeerInfo, node_id):#, node_type:NodeType):
        self.chain = Chain()
        # self.type = node_type
        self.handler = CommandHandler(self)
        self.peer = Peer(peer_info,command_handler=self.handler)
        self.peer.start_listening()
        self.node_id = node_id
    
    def make_connection(self, peer_info: PeerInfo):
        self.peer.make_connection(peer_info)
        self.send_command(11,len(self.chain.blocks))

    def initialize(self):
        # self.load_bchain()
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
        # if not self.chain.add_block(block):
        #     self.peer.broadcast_command(12, "x")
        if not self.chain.verify_last_block():
            self.chain.remove_last_block()

    def c_new_transaction(self, transaction:Transaction):
        if not self.chain.is_in_chain(transaction):
            self.chain.register_transaction(transaction)

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
        # if not self.chain.is_in_chain(transaction):
        #     if not self.chain.register_transaction(transaction):
        #         self.chain.add_new_block()
        #         self.peer.broadcast_command(21,self.chain.blocks[-1])
        #         print("Adding new block")
        if self.chain.blocks[-1].is_full():
            self.chain.add_new_block()
            self.chain.register_transaction(transaction)
            print("Adding new block")
            return False
        else:
            self.chain.register_transaction(transaction)
            return True


class GovernmentNode(Node):

    def create_passport(self,passport_id, date_from, date_to, country):
        new_passport = Transaction('p',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        if self.append_transaction(new_passport):
            self.peer.broadcast_command(31,new_passport)
        else:
            self.peer.broadcast_command(21,self.chain.blocks[-1])

    def edit_passport(self,passport_id, date_from, date_to, country):
        edited_passport = Transaction('r',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # self.append_transaction(edited_passport)
        # self.peer.broadcast_command(32,edited_passport)
        if self.append_transaction(edited_passport):
            self.peer.broadcast_command(32,edited_passport)
        else:
            self.peer.broadcast_command(21,self.chain.blocks[-1])

    def create_visa(self,passport_id, date_from, date_to, country):
        new_visa = Transaction('v',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # self.append_transaction(new_visa)
        # self.peer.broadcast_command(51, new_visa)
        if self.append_transaction(new_visa):
            self.peer.broadcast_command(51,new_visa)
        else:
            self.peer.broadcast_command(21,self.chain.blocks[-1])

class BorderControlNode(Node):

    def register_border_crossing(self,passport_id, date_from, date_to, country):
        border_crossing = Transaction('b',passport_id, date_from, date_to, country, self.node_id,self.chain.sk)
        # self.append_transaction(border_crossing)
        # self.peer.broadcast_command(41, border_crossing)
        if self.append_transaction(border_crossing):
            self.peer.broadcast_command(41, border_crossing)
        else:
            self.peer.broadcast_command(21,self.chain.blocks[-1])

class EnforcementNode(Node):

    pass

class APINode(Node):

    pass