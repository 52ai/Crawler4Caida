# coding:utf-8
"""
create on Mar 9, 2022 by Wayne YU

Function:
统计ip量
"""
from IPy import IP


def analysis():
    prefix_file = "../000LocalData/RU&UA/Level3_outage_ip.txt"
    file_read = open(prefix_file, 'r', encoding='utf-8')
    ip_list = []  # 存储所有ip
    ip_num = 0
    for line in file_read.readlines():
        v4_prefix = line.strip()
        print(v4_prefix)
        ip_num += len(IP(v4_prefix))
        for x in IP(v4_prefix):
            ip_list.append(x)
    print(ip_num)
    print("中断前缀去重前IP量:", len(ip_list))
    print("中断前缀去重后IP量:", len(set(ip_list)))


if __name__ == "__main__":
    analysis()
