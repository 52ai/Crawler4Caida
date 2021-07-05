# coding:utf-8
"""
create on July 4, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

抽取交换中心到网络间的关系，以供星云图绘制使用

思路：
直接通过https://www.peeringdb.com/api/netixlan
抽取ix和net的对应关系，即每个ix都有哪些网络接入

形成ix组，net组，以及ix-net的关系

"""
from urllib.request import urlopen
import json
from datetime import *
import time


def generate_ix_rel():
    """
    基于PEERING DB数据抽取ix和net的对应关系
    :return:
    """
    html = urlopen(r"https://www.peeringdb.com/api/netixlan")
    html_json = json.loads(html.read())
    for item in html_json['data']:
        print(item)


if __name__ == "__main__":
    time_start = time.time()
    generate_ix_rel()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")



