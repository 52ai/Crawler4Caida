# coding:utf-8
"""
create on Apr 6, 2021 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

统计国家对外互联关系中，P2C的关系

"""

import time
import csv
import os


def write_to_csv(res_list, des_path, format_string):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param format_string:
    :return None:
    """
    print("write file<%s>..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(format_string)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country():
    """
    根据asn info信息获取AS与国家对应的字典
    :return as2country:
    """
    as2country = {}  # 存储as号到country的映射关系
    as_info_file = "../000LocalData/as_Gao/asn_info.txt"
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
    return as2country


def external_as_analysis(country_arg):
    """
    根据输入的国家，统计该国家对外互联关系中，P2C的关系
    :param country_arg:
    :return:
    """
    print(country_arg)
    as2country = gain_as2country()
    # print(as2country)
    # 获取1998-2020年间全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    return_list = []  # 存储符合条件的P2C关系
    for path_item in file_path[-1:]:
        print(path_item)
        file_read = open(path_item, 'r', encoding='utf-8')
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                line = line.strip().split('|')
                as0, as1, as_rel = str(line[0]), str(line[1]), str(line[2])
                # print(as2country[as0], as2country[as1], as_rel)
                if as2country[as0] != country_arg and as2country[as1] == country_arg and as_rel == "-1":
                    print(line)
                    return_list.append(line)
            except Exception as e:
                print(e)
    save_path = "../000LocalData/caict_display/country_Provider_" + country_arg + ".csv"
    write_to_csv(return_list, save_path, ["AS0", "AS1", "Relationships"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = ["CN"]
    for country_item in country:
        external_as_analysis(country_item)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
