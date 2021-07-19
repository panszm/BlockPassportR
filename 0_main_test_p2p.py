# Podstawowy test funkcjonalności związanych z przesyłem danych w ramach sieci peer to peer. Polega, na przesłaniu prostej wiadomości tekstowej pomiędzy węzłami.

from p2p.connection_tools import *
from p2p.peer import *
from time import sleep

peer1 = Peer(PeerInfo("127.0.0.1",20001))
peer2 = Peer(PeerInfo("127.0.0.1",20002))

peer1.start_listening()
peer2.start_listening()

peer1.make_connection(peer2.get_info())
peer2.make_connection(peer1.get_info())

peer1.broadcast_command(1,"helloFrom "+peer1.get_info()[0]+':'+str(peer1.get_info()[1]))
peer2.broadcast_command(1,"helloFrom "+peer2.get_info()[0]+':'+str(peer2.get_info()[1]))

sleep(3)

peer1.stop()
peer2.stop()