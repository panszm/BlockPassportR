from p2p.peer import Peer, PeerInfo
from bchain.node_types.node_type import NodeType
from bchain.chain import Chain
import pickle
import bchain.block
from bchain.transactions import *
from bchain.node_types.command_handler import CommandHandler

class Node:

    def __init__(self, peer_info:PeerInfo, node_type:NodeType):
        self.chain = Chain()
        self.type = node_type
        self.handler = CommandHandler(self)
        self.peer = Peer(peer_info,command_handler=self.handler)

    def initialize(self):
        self.load_bchain()
        self.peer.start_listening()

    def shutdown(self):
        self.save_bchain()
        self.peer.stop()

    def save_bchain(self, filepath="./data/bchain_data"):
        file = open(filepath, 'wb')
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
        if not self.chain.verify_last_block():
            self.chain.remove_last_block()

    def c_new_transaction(self, transaction:Transaction):
        self.chain.register_transaction(transaction)

    def c_chain_length_received(self, length, peer_info):
        if length > len(self.chain.blocks):
            self.peer.send_command(12, self.peer.get_info(), peer_info)

    def c_chain_requested(self,peer_info):
        self.peer.send_command(13,self.chain,peer_info)

    def c_chain_received(self,chain:Chain):
        if chain.verify_chain and len(chain.blocks)>len(self.chain.blocks):
            self.chain = chain

class GovernmentNode(Node):

    def create_passport(self,passport_id, date_from, date_to, country, entity_id):
        if len(self.chain.blocks)>=bchain.block.MAX_TRANSACTION_COUNT:
            self.chain.add_block(bchain.block.Block(self.chain.blocks[-1].get_hash()))
            self.peer.broadcast_command(21,self.chain.blocks[-1])
        new_passport = Transaction('p',passport_id, date_from, date_to, country, entity_id)
        self.peer.broadcast_command(31,new_passport)
        self.chain.register_transaction(new_passport)

    def edit_passport(self,passport_id, date_from, date_to, country, entity_id):
        if len(self.chain.blocks)>=bchain.block.MAX_TRANSACTION_COUNT:
            self.chain.add_block(bchain.block.Block(self.chain.blocks[-1].get_hash()))
            self.peer.broadcast_command(21,self.chain.blocks[-1])
        edited_passport = Transaction('r',passport_id, date_from, date_to, country, entity_id)
        self.peer.broadcast_command(32,edited_passport)
        self.chain.register_transaction(edited_passport)

    def create_visa(self,passport_id, date_from, date_to, country, entity_id):
        if len(self.chain.blocks)>=bchain.block.MAX_TRANSACTION_COUNT:
            self.chain.add_block(bchain.block.Block(self.chain.blocks[-1].get_hash()))
            self.peer.broadcast_command(21,self.chain.blocks[-1])
        new_visa = Transaction('v',passport_id, date_from, date_to, country, entity_id)
        self.peer.broadcast_command(51, new_visa)
        self.chain.register_transaction(new_visa)

class BorderControlNode(Node):

    def register_border_crossing(self,passport_id, date_from, date_to, country, entity_id):
        if len(self.chain.blocks)>=bchain.block.MAX_TRANSACTION_COUNT:
            self.chain.add_block(bchain.block.Block(self.chain.blocks[-1].get_hash()))
            self.peer.broadcast_command(21,self.chain.blocks[-1])
        border_crossing = Transaction('b',passport_id, date_from, date_to, country, entity_id)
        self.peer.broadcast_command(41, border_crossing)
        self.chain.register_transaction(border_crossing)

class EnforcementNode(Node):

    pass

class APINode(Node):

    pass