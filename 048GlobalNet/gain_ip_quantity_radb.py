# coding:utf-8
"""
create on Aug 3, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

临时支撑任务，按照RADB 路由前缀的格式统计电信注册的IP规模

"""

import time


def gain_ip_quantity():
    """
    按照radb的路由前缀格式，统计电信注册的IP规模
    :return:
    """
    ip_prefix_radb = "../000LocalData/as_simulate/radb前缀集合.txt"
    ip_prefix_radb_read = open(ip_prefix_radb, 'r', encoding='utf-8')
    line_cnt = 0  # 记录行数
    valid_cnt = 0  # 记录有效记录数
    invalid_cnt = 0  # 记录无效记录数
    ip_num_cnt = 0  # 根据前缀统计IP规模，用32减去网络号的长度，大约为2的N次方个地址
    for line in ip_prefix_radb_read.readlines():
        line = line.strip()
        if line.find("/") != -1:
            # 有效IP前缀行
            line = line.split("/")
            valid_cnt += 1
            net_len = int(line[1])
            ip_num_cnt += pow(2, (32-net_len))
            print(line[0], line[1], pow(2, (32-net_len)))
        else:
            # print(line)
            invalid_cnt += 1
        line_cnt += 1
    print("总的记录数(文件记录)：", line_cnt)
    print("有效记录数(IP前缀)：", valid_cnt)
    print("无效记录数（AS号码）：", invalid_cnt)
    print("总的IP规模（V4）：", ip_num_cnt)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    gain_ip_quantity()
    time_end = time.time()  # 记录结束的时间
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
