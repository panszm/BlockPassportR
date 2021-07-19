# Podstawowy test funkcjonalności blockchainu, jest to rozszerzenie testu nr 0, ponieważ węzły zamiast wiadomości tesktowych, wzajemnie przesyłają tranzakcje.

from p2p.connection_tools import *
from p2p.peer import *
from time import sleep
from bchain.node import *

pi1 = PeerInfo("127.0.0.1",20001)
pi2 = PeerInfo("127.0.0.1",20002)

node1 = GovernmentNode(pi1,"PL_1")
node2 = GovernmentNode(pi2,"PL_2")

sleep(2)

node1.make_connection(node2.peer.get_info())
node2.make_connection(node1.peer.get_info())


sleep(2)

node1.create_passport("RP_12213","04-12-2021","05-11-2021","rp")
node2.create_passport("RP_12214","04-12-2021","05-11-2021","rp")

print(node1.chain.to_string())

sleep(2)

node1.shutdown()
node2.shutdown()