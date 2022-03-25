# coding:utf-8
"""
create on Mar 14, 2022 By Wenyan YU

Function:

统计北美节点，过LINX情况

"""

import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def rib_analysis(rib_file):
    """
    分析RIB信息
    :param rib_file:
    :return:
    """
    print(rib_file)
    ixp_as = "8714"
    aim_as = ["12389", "31133"]
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if ixp_as in as_path:
            print(as_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    path_item = "..\\000LocalData\\RU&UA\\rib_beimei\\Gao0305.txt"
    rib_analysis(path_item)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
