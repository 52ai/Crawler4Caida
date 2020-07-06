# coding:utf-8
"""
Create on June 17, 2020 By Wayne YU. Using Python 3.7
Email: ieeflsyu@outlook.com

Function:
新版的重点网络界面需要重新梳理一些数据，这部分数据注重现状
主要包括ASN，排名，国别及其网络的IP规模
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
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_country_info():
    """
    根据国家的缩写，翻译为中文
    :return country_info_dict:
    """
    geo_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'
    country_info_dict = {}
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        country_info_dict[line[4]] = line[5]
    return country_info_dict


def extract_info():
    result_list = []  # 存储所需的信息
    as_list = []  # 存取AS全部的原始信息
    as2country_cn = gain_country_info()
    file_in = "../000LocalData/as_map/as_core_map_data_new20200201.csv"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    for line in file_in_read.readlines():
        line = line.strip().split("|")
        print(line)
        as_list.append(line)
    as_list.sort(reverse=True, key=lambda elem: int(elem[1]))  # 降序排列
    for i in range(0, len(as_list)):
        as_name = as_list[i][5]
        as_org = as_list[i][6]
        if not as_name:
            as_org = "/"
        if not as_name:
            as_name = "/"
        result_list.append([i+1, as_list[i][0],
                            as_name,
                            as_org,
                            as2country_cn[as_list[i][8]].strip("\""),
                            as_list[i][1]])
        # print(result_list[i])
    save_path = "../000LocalData/caict_display/as_info_format.csv"
    write_to_csv(result_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    extract_info()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start))
