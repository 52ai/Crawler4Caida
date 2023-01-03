# coding:utf-8
"""
create on Nov. 29, 2022 By Wayne YU

Function:

将AS，转换为ORG，Country

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
        writer = csv.writer(csv_file)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2info_caida():
    """
    根据Caida asn info获取as对应的机构、国家信息
    :return as2info:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2info = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2]
        as_country = line[-1]
        as2info[as_number] = [as_org, as_country]
    return as2info


def country_en2cn():
    """
    将英文缩写转为中文国家
    :return country_en2cn:
    """
    country_en2cn_file = '..\\000LocalData\\as_geo\\GeoLite2-Country-Locations-zh-CN.csv'
    en2cn = {}  # 根据en2cn的映射关系
    file_read = open(country_en2cn_file, 'r', encoding="gbk")
    for line in file_read.readlines():
        line = line.strip().split(",")
        en_str = line[4]
        cn_str = line[5]
        en2cn[en_str] = cn_str
        # print(en_str, cn_str)
    return en2cn


def gain_as_info():
    """
    根据输入的as信息，输出ORG COUNTRY
    :return:
    """
    as2info = gain_as2info_caida()
    en2cn_dict = country_en2cn()
    print(as2info["4134"])
    as_list_input_file = "../000LocalData/Support4WZF/as_list_input.csv"
    file_read = open(as_list_input_file, 'r', encoding='utf-8')
    as2info_result = []
    for line in file_read.readlines():
        line = line.strip().split(",")
        temp_line_list = []
        # print(line[0])
        for as_str in line:
            as_org = "ZZ"
            as_country = "ZZ"
            try:
                as_info = as2info[as_str]
                as_org = as_info[0]
                as_country = en2cn_dict[as_info[1]]
            except Exception as e:
                print(e)
            temp_line_list.append([as_str, as_org, as_country])

        print(temp_line_list)
        as2info_result.append(temp_line_list)
    save_file = "..\\000LocalData\\Support4WZF\\as2info_result_multi.csv"
    write_to_csv(as2info_result, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    gain_as_info()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
