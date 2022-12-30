# coding:utf-8
"""
create on Dec 6, 2022 By Wayne YU

Function:

将as rel 处理成as1, country1, as2, country2, rel_type

"""

import os
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


def deal(open_file):
    """
    按要求处理as rel数据
    :param open_file:
    :return:
    """
    as2info = gain_as2info_caida()
    en2cn_dict = country_en2cn()
    print(as2info["4134"])
    file_read = open(open_file, 'r', encoding='utf-8')
    except_info = []  # 存储异常记录
    global_as_relationships_result = []
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        as0 = line.strip().split('|')[0]
        as1 = line.strip().split('|')[1]
        rel_type = line.strip().split('|')[2]
        rel_type_str = "PEER" if rel_type == "0" else "TRANSIT"

        as0_country = "查无"
        as1_country = "查无"

        try:
            as0_country = en2cn_dict[as2info[as0][1]]
        except Exception as e:
            except_info.append(e)

        try:
            as1_country = en2cn_dict[as2info[as1][1]]
        except Exception as e:
            except_info.append(e)

        temp_line = [as0, as0_country, as1, as1_country, rel_type_str]
        # print(temp_line)
        global_as_relationships_result.append(temp_line)
    save_path = "..//000LocalData//Support4ZMS//global_as_relationships_result.csv"
    write_to_csv(global_as_relationships_result, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    deal(file_path[-1])
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
