# coding:utf-8
"""
create on May 28, 2020 By Wenyan YU
Function:

该程序的目的在于通过时间维度上RIB快照信息，构建本地路由可信源
输入为N个RIB快照文件
输出为Prefix（A） Matrix(M*N)，A为在快照中任意一个出现过的前缀，M为该前缀源的个数，N为快照的个数

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


def build_prefix2as_matrix(prefix2as_matrix, rib_file):
    """
    根据传入的rib快照信息，不断更新prefix2as_matrix信息
    :param prefix2as_matrix:
    :param rib_file:
    :return:
    """
    print(rib_file)
    rib_info_prefix2as = {}  # 存储prefix2as的记录
    line_cnt = 0
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        line_cnt += 1
        origin_as = line[7].split(" ")[-1]
        # 判断key（前缀）是否在字典中
        if line[5] not in rib_info_prefix2as.keys():
            # 若前缀不在字典中，则新建记录
            rib_info_prefix2as.setdefault(line[5], []).append(origin_as)
        else:
            # 若前缀在字典中，则需要判断origin AS是否存在
            if origin_as not in rib_info_prefix2as[line[5]]:
                rib_info_prefix2as.setdefault(line[5], []).append(origin_as)
            else:
                pass
        if line_cnt >= 1000:
            pass
    print("Prefix All Records(Origin AS):", len(rib_info_prefix2as))
    prefix2as_matrix_re = prefix2as_matrix
    for key_item in rib_info_prefix2as.keys():
        if key_item not in prefix2as_matrix_re.keys():
            prefix2as_matrix_re.setdefault(key_item, []).extend(rib_info_prefix2as[key_item])
        else:
            prefix2as_matrix_re.setdefault(key_item, []).extend(rib_info_prefix2as[key_item])
    return prefix2as_matrix_re


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    rib_file_in_list = ["../000LocalData/BGPData/birdmrt_master_2020-05-07_00_45_09_M.txt",
                        "../000LocalData/BGPData/birdmrt_master_2020-05-08_00_45_09_M.txt",
                        "../000LocalData/BGPData/birdmrt_master_2020-05-09_00_45_09_M.txt"]
    # rib_file_in_list = ["../000LocalData/BGPData/birdmrt_master_2020-05-07_00_45_09_M.txt",
    #                     "../000LocalData/BGPData/birdmrt_master_2020-05-08_00_45_09_M.txt"]
    prefix2as_matrix = {}  # 存储所有的prefix2as矩阵字典，key为prefix，value为路由源AS和prefix是否在快照中出现组成的矩阵
    # 循环读取RIB文件，并构建prefix2as_matrix
    for rib_file in rib_file_in_list:
        prefix2as_matrix = build_prefix2as_matrix(prefix2as_matrix, rib_file)
    print("Prefix All Records(Origin AS):", len(prefix2as_matrix))
    for key in prefix2as_matrix.keys():
        if (len(prefix2as_matrix[key]) > 4) and ((len(prefix2as_matrix[key]) % 2) != 0):
            print(prefix2as_matrix[key])
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
