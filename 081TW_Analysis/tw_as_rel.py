# coding:utf-8
"""
create on May 6, 2022 By Wayne YU
Functon:

分析TW地区活跃自治域数量、自治域网络通告的IP地址规模、自治域网络的互联关系情况

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


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org.split(",")[0]
    return as2org_dic


def as_analysis(aim_country):
    """
    根据输入国家，获取该国家的自治域网络数量、以及各自的互联关系
    :param aim_country:
    :return:
    """
    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()
    print(f"- - - - - - - {aim_country}- - - - - -  - - ")
    # 获取1998-2022年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    except_info = []  # 存储异常信息
    for path_item in file_path[-1:]:
        print(path_item)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    country = "TW"
    as_analysis(country)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
