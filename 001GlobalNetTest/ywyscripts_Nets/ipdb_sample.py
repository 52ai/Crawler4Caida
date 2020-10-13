# coding:utf8
"""
create on Oct 13, 2020 By Wenyan YU
Function:
利用IPDB离线库，查询IP地址详细信息
"""

from ipdb import City


db = City("mydata4vipday2_cn.ipdb")
print("ipdb.build.time:", db.build_time())
print(db.find("133.130.115.224", "CN"))

