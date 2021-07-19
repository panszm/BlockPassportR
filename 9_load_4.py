# Test sprawdzający poprawność działania przy zwiększonej ilości węzłów.

from p2p.connection_tools import *
from p2p.peer import *
from time import sleep
from bchain.node import *

pi1 = PeerInfo("127.0.0.1",20001)
pi2 = PeerInfo("127.0.0.1",20002)
pi3 = PeerInfo("127.0.0.1",20003)
pi4 = PeerInfo("127.0.0.1",20004)
pi5 = PeerInfo("127.0.0.1",20005)
pi6 = PeerInfo("127.0.0.1",20006)

UrzadWojewodzki = GovernmentNode(pi1,"PL_1")
AmbasadaUS = GovernmentNode(pi2,"US_1")
PrzejscieGraniczne = BorderControlNode(pi3,"US_B_1")
PrzejscieGraniczne2 = BorderControlNode(pi4,"US_B_2")
PrzejscieGraniczne3 = BorderControlNode(pi5,"US_B_3")
PrzejscieGraniczne4 = BorderControlNode(pi6,"US_B_4")

sleep(2)

UrzadWojewodzki.make_connection(AmbasadaUS.peer.get_info())
UrzadWojewodzki.make_connection(PrzejscieGraniczne.peer.get_info())
UrzadWojewodzki.make_connection(PrzejscieGraniczne2.peer.get_info())
UrzadWojewodzki.make_connection(PrzejscieGraniczne3.peer.get_info())
UrzadWojewodzki.make_connection(PrzejscieGraniczne4.peer.get_info())

AmbasadaUS.make_connection(UrzadWojewodzki.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne2.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne3.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne4.peer.get_info())

PrzejscieGraniczne.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne.make_connection(AmbasadaUS.peer.get_info())
PrzejscieGraniczne.make_connection(PrzejscieGraniczne2.peer.get_info())
PrzejscieGraniczne.make_connection(PrzejscieGraniczne3.peer.get_info())
PrzejscieGraniczne.make_connection(PrzejscieGraniczne4.peer.get_info())

PrzejscieGraniczne2.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne2.make_connection(AmbasadaUS.peer.get_info())
PrzejscieGraniczne2.make_connection(PrzejscieGraniczne.peer.get_info())
PrzejscieGraniczne2.make_connection(PrzejscieGraniczne3.peer.get_info())
PrzejscieGraniczne2.make_connection(PrzejscieGraniczne4.peer.get_info())

PrzejscieGraniczne3.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne3.make_connection(AmbasadaUS.peer.get_info())
PrzejscieGraniczne3.make_connection(PrzejscieGraniczne2.peer.get_info())
PrzejscieGraniczne3.make_connection(PrzejscieGraniczne.peer.get_info())
PrzejscieGraniczne3.make_connection(PrzejscieGraniczne4.peer.get_info())

PrzejscieGraniczne4.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne4.make_connection(AmbasadaUS.peer.get_info())
PrzejscieGraniczne4.make_connection(PrzejscieGraniczne2.peer.get_info())
PrzejscieGraniczne4.make_connection(PrzejscieGraniczne3.peer.get_info())
PrzejscieGraniczne4.make_connection(PrzejscieGraniczne.peer.get_info())

sleep(2)

for i in range(0,100):
    UrzadWojewodzki.create_passport("pl_ae12sada12__"+str(i)+"__","2020-03-01","2027-03-02","PL")
    sleep(0.1)
    AmbasadaUS.create_passport("pl_ae12sada12__"+str(i)+"__","2020-03-01","2027-03-02","PL")
    sleep(0.1)
    PrzejscieGraniczne.register_border_crossing("pl_ae12sada12__"+str(i)+"__","2020-03-01","2027-03-02","PL")
    sleep(0.1)

sleep(2)

print(PrzejscieGraniczne3.chain.to_string())

sleep(2)

UrzadWojewodzki.shutdown()
AmbasadaUS.shutdown()
PrzejscieGraniczne.shutdown()
PrzejscieGraniczne2.shutdown()
PrzejscieGraniczne3.shutdown()
PrzejscieGraniczne4.shutdown()