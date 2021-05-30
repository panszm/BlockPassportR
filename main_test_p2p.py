from p2p.connection_tools import *
from p2p.peer import *

peer1 = Peer(PeerInfo("127.0.0.1",20001))
peer2 = Peer(PeerInfo("127.0.0.1",20002))

peer1.start_listening()
peer2.start_listening()

peer1.make_connection(peer2.get_info())
peer2.make_connection(peer1.get_info())

peer1.broadcast_message("helloFrom "+peer1.get_info()[0]+':'+str(peer1.get_info()[1]))
peer2.broadcast_message("helloFrom "+peer2.get_info()[0]+':'+str(peer2.get_info()[1]))

peer1.stop_listening()
peer2.stop_listening()