# coding:utf-8
"""
create on Mar 5, 2022 By Wayne YU

Function:

研究发现Cogent中断的事件

"""

import time
import csv
import os


def gain_as2country():
    """
    获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info.txt'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_name = line[1].strip().split(",")[0].strip()
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
    return as2country


def rib_analysis():
    """
    分析RIB信息，发现Cogent(AS174)与俄网络的互联关系
    :return:
    """
    as2country_dic = gain_as2country()
    print("AS12389's Country:", as2country_dic['12389'])
    rib_file = "..\\000LocalData\\RU&UA\\z0215.txt"
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        as_path = line[-2].split(" ")
        # print(as_path)
        """
        对每个Path做分析
        """
        if "174" in as_path:
            # print(as_path)
            for i in range(0, len(as_path)-1):
                # print(as_path[i], as_path[i+1])
                try:
                    if as_path[i] == "174":
                        if as2country_dic[as_path[i+1]] == "RU":
                            print(as_path[i], as_path[i+1])
                    if as_path[i+1] == "174":
                        if as2country_dic[as_path[i]] == "RU":
                            print(as_path[i], as_path[i+1])
                except Exception as e:
                    # print(e)
                    pass


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_analysis()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")