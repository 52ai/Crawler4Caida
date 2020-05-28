# coding:utf-8
"""
create on May 28, 2020 By Wenyan YU
Function:

在处理RIPE BGP路由历史数据时，与Bird系统存在一定的差异
如果把所有事都放在bird_analysis.py里面做，还是比较繁琐的，因此写一个程序去将RIPE BGP数据处理成Bird系统数据格式

"""
import csv
import time


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def format_ripe_message(message_file):
    """
    根据传入的RIPE message file数据，统一处理成Bird的数据格式
    :param message_file:
    :return:
    """
    print(message_file)
    des_list = []  # 存储目标格式的数据\
    file_read = open(message_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        line.insert(6, 'rr0')
        des_list.append(line)
    # 将目标格式的数据持久化
    save_path = '../000LocalData/BGPData/updates.20200526.1010_M_Bird.txt'
    write_to_csv(des_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    message_file_in = '../000LocalData/BGPData/updates.20200526.1010_M.txt'
    format_ripe_message(message_file_in)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")