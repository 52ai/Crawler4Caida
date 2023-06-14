# coding:utf-8
"""
create on Jun 12, 2023 by Wayne YU
Function:

开发31省三家运营商PING测试探针程序

"""
from ping3 import ping
import time
from ipdb import City
import requests
import re


def gain_ip_list():
    """
    根据31省监测节点表获取IP地址信息，共计93个
    :return ip_list:
    """
    ip_list = []
    ip_file = "../000LocalData/104PING31PTask/ip_info_file.csv"
    with open(ip_file, "r", encoding="gbk") as f:
        for item in f.readlines()[1:]:
            ip_list.append(item.strip().split(","))
    return ip_list


if __name__ == '__main__':

    time_start = time.time()
    time_format = "%Y%m%d %H:%M:%S"
    time_str = time.strftime(time_format, time.localtime())
    print("=======>启动探测：", time_str)

    db = City("../000LocalData/ipdb/caict_ipv4.ipdb")
    print("ipdb.build.time:", db.build_time())

    # 获取公网IP地址
    req = requests.get("http://txt.go.sohu.com/ip/soip")
    ip_public = re.findall(r'\d+.\d+.\d+.\d+', req.text)[0]

    print("Public IP:", ip_public, db.find(ip_public, "CN"))

    iter_cnt = 1
    iter_cnt_max = 3
    while iter_cnt_max:
        for line in gain_ip_list():
            temp_line = []
            # print(db.find(line[-1], "CN"))
            delay = ping(line[-1], timeout=1, size=100)
            temp_line.append(iter_cnt)
            temp_line.append(ip_public)
            temp_line.append(time.strftime(time_format, time.localtime()))
            temp_line.extend(line)
            temp_line.append(delay)
            print(temp_line)
        iter_cnt += 1
        iter_cnt_max -= 1
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
