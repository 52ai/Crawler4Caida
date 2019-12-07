# coding:utf-8
"""
create on Dec 6, 2019 by  Wayne Yu
Function:

实现AS Core Map的绘制

1）通过AS-relationship文件，获取到当前时间的所有活跃AS号，及其AS连接数
2）根据活跃的号列表去IPIP网站抓取ASName、Org Name、IPv4Prefixes、IPv6Prefixes、IPv4 Nums、IPv6 Nums、Registry Region
3）根据Registry Region的信息去201603.location.txt中抓取经纬度信息
4）根据AS连接数，以及AS的进度信息，去计算极坐标的angle和radius
5）使用matplotlib绘图
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
        writer = csv.writer(csvFile)
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


def gain_as_info(page_url):
    """
    根据as的页面地址，去获取as的详细信息
    :param page_url:
    :return as_info_list:
    """
    as_info_list = []
    driver.get(page_url)
    # time.sleep(3)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    bsObj = BeautifulSoup(page_html, "html.parser")
    # ===========获取该AS号的AS info==============
    td_list = bsObj.find("table", {"class": "table table-bordered"}).findAll("td")
    as_name = td_list[0].get_text()
    org_name = td_list[1].get_text()
    ipv4_prefixes = locale.atoi(td_list[2].get_text())
    ipv6_prefixes = locale.atoi(td_list[3].get_text())
    ipv4_nums = locale.atoi(td_list[4].get_text())
    ipv6_nums = locale.atoi(td_list[5].get_text())
    registry_region = td_list[6].find("a").attrs['href'].split('/')[-1]

    as_info_list.append(as_name)
    as_info_list.append(org_name)
    as_info_list.append(ipv4_prefixes)
    as_info_list.append(ipv6_prefixes)
    as_info_list.append(ipv4_nums)
    as_info_list.append(ipv6_nums)
    as_info_list.append(registry_region)
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
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    date_string, as_active_list = gain_active_as(file_path[0])
    print("活跃的AS号数量：", len(as_active_list))
    # print(as_active_list)
    # 根据as_active_list去IPIP网站获取AS详细信息，包括Registry Region
    # 启动浏览器
    driver = webdriver.Firefox()
    as_core_map_data = []
    as_temp = []
    for as_item in as_active_list:
        try:
            as_temp.append(as_item)
            as_rel = gain_as_relationships_cnt(as_item, file_path[0])  # 计算as的BGP互联关系
            as_temp.extend(as_rel)
            as_url = "https://whois.ipip.net/AS"+as_item
            as_info = gain_as_info(as_url)  # 通过IPIP网站获取as info
            # print(as_info)
            as_temp.extend(as_info)
            as_geo = gain_as_geo(as_info[-1])
            as_temp.extend(as_geo)
        except Exception as e:
            print(e, "|", as_url)
        finally:
            print(as_temp)
            as_core_map_data.append(as_temp)
            as_temp = []
    # 关闭浏览器
    driver.quit()
    # 存储as_core_map_data文件
    save_path = './as_core_map_data.csv'
    write_to_csv(as_core_map_data, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
