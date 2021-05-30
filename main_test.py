from p2p.connection_tools import *
from p2p.peer import *

peer1 = Peer(PeerInfo("127.0.0.1",20001))
peer2 = Peer(PeerInfo("127.0.0.1",20002))

peer1.start_listening()


peer1.stop_listening()