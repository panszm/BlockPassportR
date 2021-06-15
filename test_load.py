from p2p.connection_tools import *
from p2p.peer import *
from time import sleep
from bchain.node import *

pi1 = PeerInfo("127.0.0.1",20001)
pi2 = PeerInfo("127.0.0.1",20002)
pi3 = PeerInfo("127.0.0.1",20003)

UrzadWojewodzki = GovernmentNode(pi1,"PL_1")
AmbasadaUS = GovernmentNode(pi2,"US_1")
PrzejscieGraniczne = BorderControlNode(pi3,"US_B_1")

sleep(2)

UrzadWojewodzki.make_connection(AmbasadaUS.peer.get_info())
UrzadWojewodzki.make_connection(PrzejscieGraniczne.peer.get_info())
AmbasadaUS.make_connection(UrzadWojewodzki.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne.peer.get_info())
PrzejscieGraniczne.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne.make_connection(AmbasadaUS.peer.get_info())

sleep(2)
for i in range(1,100):
    UrzadWojewodzki.create_passport("pl_ae12sada12__"+str(i)+"__","2020-03-01","2027-03-02","PL")
    sleep(0.1)

sleep(2)

print(AmbasadaUS.chain.to_string())
print("UW ",len(UrzadWojewodzki.chain.blocks))
print("AU ",len(AmbasadaUS.chain.blocks))
print("PG ",len(PrzejscieGraniczne.chain.blocks))

sleep(2)

UrzadWojewodzki.shutdown()
AmbasadaUS.shutdown()
PrzejscieGraniczne.shutdown()