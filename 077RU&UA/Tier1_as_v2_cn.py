# coding:utf-8

"""
create on Mar 7, 2020 by Wayne YU
Function:

从中国、北美出发去往俄罗斯的网络，统计其中经Cogent（即Tier1）中的占的比例，进而分析全球AS网络受影响的比例


V2，修改策略
Tier1断俄罗斯的直联的影响，需要关联分析

V2_cn，推广至CN，或其他国家
1）将RU，推广至CN，即去往全球各网络的路径数量，其中需要经Tier1的路径数量，取一个比例，进而推算每个网络受影响的比例
2）地址量计算，存在大小段重复统计的问题，可以做一些特殊的处理，先散列成IP，再做去重

结论：分析中国的结论，需要重新搞，这个通过路径的思路也存在问题

"""

import time
import csv
import os
from IPy import IP


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
    分析RIB信息，分析经Tier1与其他国家的互联关系
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country()
    print("AS12389's Country:", as2country_dic['12389'])

    # tier1_list = ['174']

    tier1_list = ['3356', '174', '2914', '6939', '3257', '701', '7018', '1239', '3549', '7922']

    # tier1_list = ['3356', '174', '2914', '6939', '3257',
    #               '701', '7018', '1239', '3549', '7922',
    #               '3320', '6830', '5511', '3491', '6762',
    #               '1299', '12956', '6461']

    analysis_country = "CN"
    print("Analysis Country:", analysis_country)

    """
    1）统计到达所有AS网络前缀及其路径
    """
    as_dict = {}
    """
    以目的ASN作为key，[[ip_prefix, as_path], ...]作为value
    构建中国、北美去往全球目的ASN的前缀和路径
    """
    file_read = open(rib_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if as_path[0] != "4837":
            continue
        origin_as = as_path[-1]
        # print(origin_as, v4_prefix, as_path)
        if origin_as not in as_dict.keys():
            as_dict[origin_as] = [[v4_prefix, as_path]]
        else:
            as_dict[origin_as].append([v4_prefix, as_path])
    print("ORIGIN ASN COUNT:", len(as_dict.keys()))

    """
    2）统计所有AS网络的路径中，经Tier1的数量（1）
    
    asn, country, v4_prefix_list, all_path, tier1_path
    
    """
    result_list = []  # 存储结果数据
    for key in as_dict.keys():
        # print(key, as_dict[key])
        asn = key
        country = "ZZ"
        try:
            country = as2country_dic[asn]
        except Exception as e:
            # print(e)
            pass
        v4_prefix_list = []  # 存储所有v4前缀，去重后的
        all_path = 0  # 存储所有all_path的数量
        tier1_path = 0  # 存储经过tier1路径的数量
        for line in as_dict[key]:
            v4_prefix = line[0]
            as_path = line[1]

            if v4_prefix not in v4_prefix_list:
                v4_prefix_list.append(v4_prefix)
            all_path += 1  # 全部路径数量自增1
            """
            需要关联Tier1与某国家网络的直联关系
            """
            if set(as_path).intersection(set(tier1_list)):
                for i in range(0, len(as_path) - 1):
                    try:
                        if as_path[i] in tier1_list:
                            if as2country_dic[as_path[i+1]] == analysis_country:
                                tier1_path += 1

                        if as_path[i+1] in tier1_list:
                            if as2country_dic[as_path[i]] == analysis_country:
                                tier1_path += 1
                    except Exception as e:
                        pass

        result_list.append([asn, country, v4_prefix_list, all_path, tier1_path])

    # print(result_list)

    """
    3）统计所有AS网络的路径中，经Tier1的数量（2）

    asn, country, v4_num, all_path, tier1_path, rate

    """
    result_list_final = []  # 存储最终结果数据
    for item in result_list:
        # print(item[0], item[1], len(item[2]), item[3], item[4])
        asn = item[0]
        if item[0].find("{") != -1:
            # print(item[0])
            asn = item[0].strip("{").strip("}").split(",")[0]
        # print(asn)
        v4_num = 0  # 存储该网的IPv4地址数量
        for v4_prefix in item[2]:
            v4_num += len(IP(v4_prefix))
        # print(v4_num)
        rate = item[4] / item[3]
        result_list_final.append([asn, item[1], v4_num, item[3], item[4], rate, round(v4_num*rate)])
        print([asn, item[1], v4_num, item[3], item[4], rate, round(v4_num*rate)])

    write_to_csv(result_list_final, "..\\000LocalData\\RU&UA\\result_final_v2_cn.txt")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    path_item = "..\\000LocalData\\RU&UA\\rib\\z0224.txt"
    rib_analysis(path_item)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
