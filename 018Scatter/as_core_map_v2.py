# coding:utf-8
"""
create on Dec 6, 2019 by  Wayne Yu
Version:2
Function:

实现AS Core Map的绘制

1）通过AS-relationship文件，获取到当前时间的所有活跃AS号，及其AS连接数
2）根据活跃的号列表去as-org2info表中去获取as info ，包括AS name, Org name，Country
3）根据Country的信息去201603.location.txt中抓取经纬度信息
4）根据AS连接数，以及AS的进度信息，去计算极坐标的angle和radius
5）使用matplotlib绘图

#aut|changed|aut_name|org_id|opaque_id|source
#org_id|changed|org_name|country|source
"""
import os
import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # 用来配置地域信息，尽量少使用，会影响线程的安全性


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


def gain_active_as(open_file):
    """
    根据输入的AS互联关系数据，获取当前时间活跃的AS列表
    :param open_file:
    :return:
    """
    print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        """
        # if line.strip().split('|')[0] not in as_list:
        #     as_list.append(line.strip().split('|')[0])
        # if line.strip().split('|')[1] not in as_list:
        #     as_list.append(line.strip().split('|')[1])
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    # print(as_list)
    # print("Active AS：", len(as_list))
    return date_str, as_list


def gain_as_relationships_cnt(asn, open_file):
    """
    根据传入的asn,统计其bgp互联关系(All, Peer, Transit)
    :param asn:
    :param open_file:
    :return rel:
    """
    rel = []
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_provider_cnt = 0
    transit_customer_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[0] == asn:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

        if line.strip().split('|')[1] == asn:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1
    rel.append(edge_cnt)
    rel.append(peer_cnt)
    rel.append(transit_provider_cnt)
    rel.append(transit_customer_cnt)
    return rel


def gain_as_info(asn):
    """
    根据as-org2info文件，去获取as的详细信息
    :param asn:
    :return as_info_list:
    """
    as_info_list = []
    as_org2info_file = "..\\000LocalData\\as_geo\\20190701.as-org2info.txt"
    as_org2info_asn_file = "..\\000LocalData\\as_geo\\20190701.as-org2info-asn.txt"
    as_org2info_read = open(as_org2info_file, 'r', encoding='utf-8')
    as_org2info_asn_read = open(as_org2info_asn_file, 'r', encoding='utf-8')
    org_id = ""
    for line in as_org2info_asn_read.readlines():
        if line.strip().split("|")[0] == asn:
            org_id = line.strip().split("|")[3]
            as_info_list.append( line.strip().split("|")[2])  # as name
            break
    for line in as_org2info_read.readlines():
        if line.strip().split("|")[0] == org_id:
            as_info_list.append(line.strip().split("|")[2])  # org name
            as_info_list.append(line.strip().split("|")[4])  # source
            as_info_list.append(line.strip().split("|")[3])  # country
            break
    return as_info_list


def gain_as_geo(asn_country):
    """
    根据传入的as国家（地区信息）获取其经纬度
    :param asn_country:
    :return geo_list:
    """
    geo_file = "..\\000LocalData\\as_geo\\201603.locations.txt"
    geo_list = []
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as_country = line.strip().split("|")[2]
        if as_country == asn_country:
            geo_list.append(line.strip().split("|")[5])  # 获取维度
            geo_list.append(line.strip().split("|")[6])  # 获取经度
            return geo_list  # 找到后直接结束函数，并返回
    # 没有找到则设置一个默认值
    print(asn_country, "is not found in geo file!")
    geo_list.append("0.0")
    geo_list.append("0.0")
    return geo_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    active_as = []  # 记录活跃的as号
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-3"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    for path_item in file_path[3:]:
        date_string, as_active_list = gain_active_as(path_item)
        print("活跃的AS号数量：", len(as_active_list))
        # print(as_active_list)
        as_core_map_data = []
        as_temp = []
        # cnt = 10
        for as_item in as_active_list:
            # cnt -= 1
            # if cnt == 0:
            #     break
            try:
                as_temp.append(as_item)
                as_rel = gain_as_relationships_cnt(as_item, path_item)  # 计算as的BGP互联关系
                as_temp.extend(as_rel)
                as_info = gain_as_info(as_item)  # 获取as info
                # print(as_info)
                as_temp.extend(as_info)
                as_geo = gain_as_geo(as_info[-1])
                as_temp.extend(as_geo)
                print(as_temp)
                as_core_map_data.append(as_temp)
            except Exception as e:
                print(e)
            finally:
                # print(as_temp)
                as_core_map_data.append(as_temp)
                as_temp = []
        # 存储as_core_map_data文件
        save_path = '..\\000LocalData\\as_map\\as_core_map_data_' + date_string + '.csv'
        write_to_csv(as_core_map_data, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
