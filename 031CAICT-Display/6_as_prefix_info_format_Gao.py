# coding:utf-8
"""
Create on July 28, 2020 By Wayne YU. Using Python 3.7
Email: ieeflsyu@outlook.com

Function:

V2:
在第一个版本的基础上，新增高总数据的版本，仅有AS号和汉化的国家

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
    file_in = "../000LocalData/as_Gao/asn_info.txt"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    for line in file_in_read.readlines():
        line = line.strip().split("\t")
        print(line[1].split(","))
    save_path = "../000LocalData/caict_display/as_info_format_Gao.csv"
    write_to_csv(result_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    extract_info()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start))
