from p2p.peer import Peer, PeerInfo
from bchain.chain import Chain
import pickle

class Node:

    def __init__(self, peer_info:PeerInfo, node_options):
        self.chain = Chain()
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