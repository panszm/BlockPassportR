from p2p.connection_tools import *
from p2p.peer import *
from time import sleep
from bchain.node import *

pi1 = PeerInfo("127.0.0.1",20001)
pi2 = PeerInfo("127.0.0.1",20002)

node1 = GovernmentNode(pi1)
node2 = GovernmentNode(pi2)

sleep(2)

node1.make_connection(node2.peer.get_info())
node2.make_connection(node1.peer.get_info())

node1.send_command(1,"helloFrom "+pi1.get_info()[0]+':'+str(pi1.get_info()[1]))
node2.send_command(1,"helloFrom "+pi2.get_info()[0]+':'+str(pi2.get_info()[1]))

sleep(2)

node1.shutdown()
node2.shutdown()