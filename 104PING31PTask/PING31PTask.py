# coding:utf-8
"""
create on Jun 12, 2023 by Wayne YU
Function:

开发31省三家运营商PING测试探针程序

"""
from ping3 import ping, verbose_ping
import time


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

    result_list = []
    for line in gain_ip_list():
        temp_line = []
        delay = ping(line[-1], timeout=1, size=100)
        temp_line.append(time.strftime(time_format, time.localtime()))
        temp_line.extend(line)
        temp_line.append(delay)
        print(temp_line)

    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")

