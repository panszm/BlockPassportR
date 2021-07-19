# Test sprawdzający poprawność działania w sytuacji, gdy węzeł zostanie przyłączony w trakcie przesyłu.

from p2p.connection_tools import *
from p2p.peer import *
from time import sleep
from bchain.node import *

pi1 = PeerInfo("127.0.0.1",20001)
pi2 = PeerInfo("127.0.0.1",20002)
pi3 = PeerInfo("127.0.0.1",20003)

UrzadWojewodzki = GovernmentNode(pi1,"PL_1")
AmbasadaUS = GovernmentNode(pi2,"US_1")

sleep(2)

UrzadWojewodzki.make_connection(AmbasadaUS.peer.get_info())
AmbasadaUS.make_connection(UrzadWojewodzki.peer.get_info())

sleep(2)

UrzadWojewodzki.create_passport("pl_ae12sada12","2020-03-01","2027-03-02","PL")
AmbasadaUS.create_visa("pl_ae12sada12","2021-04-05","2022-01-05","US")
PrzejscieGraniczne = BorderControlNode(pi3,"US_B_1")

UrzadWojewodzki.make_connection(PrzejscieGraniczne.peer.get_info())
AmbasadaUS.make_connection(PrzejscieGraniczne.peer.get_info())
PrzejscieGraniczne.make_connection(UrzadWojewodzki.peer.get_info())
PrzejscieGraniczne.make_connection(AmbasadaUS.peer.get_info())

UrzadWojewodzki.edit_passport("pl_ae12sada12","2021-05-05","2027-03-02","PL")
PrzejscieGraniczne.register_border_crossing("pl_ae12sada12","2022-06-07","","US")

sleep(2)

print(PrzejscieGraniczne.chain.to_string())

sleep(2)

UrzadWojewodzki.shutdown()
AmbasadaUS.shutdown()
PrzejscieGraniczne.shutdown()