from p2p.peer import Peer, PeerInfo
from bchain.node_types.node_type import NodeType
from bchain.chain import Chain
import pickle
import bchain.block
import bchain.transactions

class Node:

    def __init__(self, peer_info:PeerInfo, node_type:NodeType):
        self.chain = Chain()
        self.type = node_type
        self.peer = Peer(peer_info)

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

    def c_new_transaction(self, transaction:bchain.transactions.Transaction):
        self.chain.register_transaction(transaction)

    def c_chain_length_received(self, length, peer_info):
        if length > len(self.chain.blocks):
            self.peer.send_command(12, self.peer.get_info(), peer_info)

    def c_chain_requested(self,peer_info):
        self.peer.send_command(13,self.chain,peer_info)

    def c_chain_received(self,chain:Chain):
        if chain.verify_chain and len(chain.blocks)>len(self.chain.blocks):
            self.chain = chain

class Node2(Node):

    pass