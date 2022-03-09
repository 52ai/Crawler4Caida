# coding:utf-8
"""
create on Mar 5, 2022 By Wayne YU

Function:

研究发现Cogent中断的事件

"""

import time
import csv
import os


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    # print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    # print("write finish!")


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


def rib_analysis(rib_file):
    """
    分析RIB信息，发现Cogent(AS174)与俄网络的互联关系
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country()
    # print("AS12389's Country:", as2country_dic['12389'])
    by_as = "174"
    aim_country = "RU"
    result_list = []
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        v4_prefix = line[5]
        # print(v4_prefix)
        as_path = line[-2].split(" ")
        # print(as_path)
        temp_line = [v4_prefix]
        temp_line.extend(as_path)
        """
        对每个Path做分析
        """
        if by_as in as_path:
            # print(as_path)
            for i in range(0, len(as_path)-1):
                # print(as_path[i], as_path[i+1])
                try:
                    if as_path[i] == by_as:
                        if as2country_dic[as_path[i+1]] == aim_country:
                            # print(as_path[i], as_path[i+1])
                            result_list.append(temp_line)
                    if as_path[i+1] == by_as:
                        if as2country_dic[as_path[i]] == aim_country:
                            # print(as_path[i], as_path[i+1])
                            result_list.append(temp_line)
                except Exception as e:
                    # print(e)
                    pass
    print("2022"+rib_file.strip().split("\\")[-1].strip(".txt").strip("z"), "路径数量：", len(result_list))
    result_file = "..\\000LocalData\\RU&UA\\as_path_statistic\\"+"result_"+rib_file.strip().split("\\")[-1].strip(".txt").strip("z")+".txt"
    write_to_csv(result_list, result_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\RU&UA\\rib"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    print("从中国出发，统计经某Tier1去往俄罗斯的路径数量")
    for path_item in file_path[-7:]:
        rib_analysis(path_item)
    time_end = time.time()
    # print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
