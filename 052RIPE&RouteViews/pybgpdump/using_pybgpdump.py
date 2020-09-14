# coding:utf-8
"""
create on Sep 11, 2020 By Wenyan YU

Function:
探索在windows端读取并分析MRT格式数据

"""

from mrtparse import *


mrt_updates = "../../000LocalData/BGPData/updates.20200809.0420.gz"
d = Reader(mrt_updates)

m = d.next()
for m in d:
    print(m.mrt.bgp.peer_as)
