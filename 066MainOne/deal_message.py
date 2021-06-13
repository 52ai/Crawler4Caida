# coding:utf-8
"""
create on Jun 13, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

处理BGP Message报文，20181112 21:00:00-20181112 22:39:59
匹配模式：4809（中国电信） 37282（MainOne） 15169(Google)

"""

import time
from IPy import IP


message_file = "../000LocalData/MainOne/updates.all.mainone.txt"


def deal_message():
    """
    处理主程序
    :return:
    """
    print("收集BGP Message报文的时间段: 20181112 21:00:00-20181112 22:39:59")
    print("匹配模式：4809（中国电信） 37282（MainOne） 15169(Google)")
    file_read = open(message_file, 'r', encoding='utf-8')
    message_count = 0
    ip_prefix = []  # 存储受影响的IP prefix列表
    for line in file_read.readlines():
        message_count += 1
        if line.find("4809 37282 15169|") != -1:
            line = line.strip().split("|")
            ip_prefix.append(line[5])
    print("接收到BGP Message报文总数量:", message_count)
    print("受影响的前缀记录：", len(ip_prefix))
    print("受影响的前缀记录（去重后）：", len(list(set(ip_prefix))))
    ip_num = 0  # 记录受影响的IP地址数量
    for item in list(set(ip_prefix)):
        # print(item, len(IP(item)))
        ip_num += len(IP(item))
    print("受影响IP地址数量统计（去重后）:", ip_num)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    deal_message()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")


