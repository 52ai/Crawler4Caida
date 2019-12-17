# coding: utf-8
"""
create on Dec 17,2019 By Wayne Yu

Function:

本程序主要用于处理并生成AS-ORG的具体信息

1）数据输入
 "..\\000LocalData\\as_geo\\20190701.as-org2info.txt"
 "..\\000LocalData\\as_geo\\20190701.as-org2info-asn.txt"
 "..\\000LocalData\\as_geo\\201603.locations.txt"
2）数据格式
#aut|changed|aut_name|org_id|opaque_id|source
#org_id|changed|org_name|country|source
3）数据输出
# asn|changed|as_name|org_name|country|source|latitude|longitude
"""

import os
import time
import csv
import numpy as np


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def deal_as_org_info(as_org_file, org_info_file, country_geo_file):
    """
    根据输入的文件信息，按需处理并提取as_org_info
    :param as_org_file:
    :param org_info_file:
    :param country_geo_file:
    :return as_org_info_list_copy:
    """
    as_org_info_list = []
    as_org_file_read = open(as_org_file, 'r', encoding='utf-8')
    org_info_file_read = open(org_info_file, 'r', encoding='utf-8')
    country_geo_file_read = open(country_geo_file, 'r', encoding='utf-8')
    list_temp = []
    for line in as_org_file_read.readlines():
        line = line.strip().split("|")
        # print(line)
        list_temp.append(line[0])
        list_temp.append(line[1])
        list_temp.append(line[2])
        list_temp.append(line[3])
        as_org_info_list.append(list_temp)
        list_temp = []
    # 读取org_info_file一次，用哈希表的方式，记录其info
    org_info_dict = {}  # 存储org info的字典
    for line in org_info_file_read.readlines():
        line = line.strip().split("|")
        org_info_dict.setdefault(line[0], []).append(line[2])
        org_info_dict.setdefault(line[0], []).append(line[3])
        org_info_dict.setdefault(line[0], []).append(line[4])
    # print(org_info_dict)
    # 根据org inf 哈希表，去生成as_org_info_list
    as_org_info_list_copy = []
    for item in as_org_info_list:
        org_id = item[3]
        del item[3]  # 删除列表中的org id部分
        item.extend(org_info_dict[org_id])
        as_org_info_list_copy.append(item)
    as_org_info_list = as_org_info_list_copy
    # 读取country_geo_file一次，用哈希表的方式，记录其经纬度，若存在多个经纬度，均需提取
    country_geo_dict = {}
    geo_data = []
    for line in country_geo_file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        # print(line)
        geo_data.append(line[-3])
        geo_data.append(line[-2])
        if line[2] == "US":  # 美国比较特殊，区分的更细
            country_geo_dict.setdefault(line[3], []).append(geo_data)
        else:
            country_geo_dict.setdefault(line[2], []).append(geo_data)
        geo_data = []

    print(country_geo_dict["KY"])
    # 根据country_geo 哈希表，去生成as_org_info_list
    as_org_info_list_copy = []
    except_country = []
    for item in as_org_info_list:
        try:
            # print(item[-2], len(country_geo_dict[item[-2]]))
            # 若AS所属机构，为EU或GB，则均以UK的经纬度作为其地理信息
            if item[-2] == "EU" or item[-2] == "GB":
                item[-2] = "UK"
            # 若美国AS所属机构，没有具体到哪个州，则以华盛顿（DC）的经纬度作为其地理信息
            if item[-2] == "US":
                item[-2] = "DC"
            max_geo_len = len(country_geo_dict[item[-2]])
            geo_index = np.random.randint(0, max_geo_len, size=1)
            # print(geo_index)
            geo_select = country_geo_dict[item[-2]][geo_index[0]]
            item.extend(geo_select)
            as_org_info_list_copy.append(item)
        except Exception as e:
            # print(e, item[-2])
            except_country.append(item[-2])
    print("无法直接获取经纬度信息的国家和地区个数：", len(set(except_country)))
    print(set(except_country))
    as_org_info_list = as_org_info_list_copy
    return as_org_info_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    as_org_file_in = "..\\000LocalData\\as_geo\\20190701.as-org2info-asn.txt"
    org_info_file_in = "..\\000LocalData\\as_geo\\20190701.as-org2info.txt"
    country_geo_file_in = "..\\000LocalData\\as_geo\\201603.locations.txt"
    as_org_info = deal_as_org_info(as_org_file_in, org_info_file_in, country_geo_file_in)
    # print(as_org_info)
    # 存储as_org_info文件
    save_path = '..\\000LocalData\\as_geo\\as_org_info.csv'
    write_to_csv(as_org_info, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


""""
无法直接获取经纬度信息的国家和地区（105个）：
{'LR', 'BL', 'GP', 'AI', 'MP', 'TL', 'DM', 'BQ', 'FK', 'MQ', 'BZ', 'BW', 'MG', 'ZM', 'MR', 'CK', 'SO', 'AS', 'BA', 'TK', 'TV', 'VC', 'CF', 'BF', 'CM', 'KI', 'FM', 'WF', 'TO', 'KM', 'PW', 'JM', 'SB', 'BB', 'CV', 'DZ', 'SR', 'ML', 'WS', 'KH', 'PS', 'RW', 'MH', 'KG', 'BI', 'GQ', 'NU', 'PG', 'CI', 'AD', 'VI', 'SN', 'TC', 'GY', 'SX', 'RE', 'CW', 'AQ', 'PF', 'ST', 'YE', 'ER', 'GM', 'HT', 'SS', 'TM', 'CG', 'GG', 'AW', 'NA', 'LY', 'IM', 'AG', 'GD', 'LC', 'BT', 'YT', 'GW', 'SM', 'ET', 'NF', 'UM', 'KP', 'JE', 'SY', 'TG', 'GF', 'MC', 'IO', 'BJ', 'TD', 'MV', 'MF', 'KN', 'GN', 'AX', 'SZ', 'BO', 'GL', 'GU', 'HN', 'TT', 'PM', 'MW', 'ZW'}
"""