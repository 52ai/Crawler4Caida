# coding:utf-8
"""
create on Nov 11, 2019 by Wayne Yu
Function: 分析全国已分配AS BGP互联关系排名

IPIP + CAIDA
"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
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


def obtain_country_asns(page_url):
    """
    根据每个国家的ASNs网页信息，抓取每个国家已经分配的ASNs信息
    :return None:
    """
    result_list = []
    # 1.获取ASNs列表
    driver.get(page_url)
    time.sleep(3)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    # print(page_html)
    bsObj = BeautifulSoup(page_html, "html.parser")
    # print(bsObj)
    # 获取该国家（地区）的AS list
    as_list = []  # 存储该国家（地区）的AS 列表信息
    as_list_item = []
    as_list_item.append("Number")
    as_list_item.append("ASN")
    as_list_item.append("Name")
    as_list_item.append("IPv4 Num IPs")
    as_list_item.append("IPv6 Num IPs(/64)")
    as_list_item.append("AsPageUrl")
    as_list.append(as_list_item)
    as_list_item = []
    rank_cnt = 1
    tr_list = bsObj.find("table").find("tbody").findAll("tr")
    for tr_item in tr_list:
        as_list_item.append(rank_cnt)
        as_list_item.append(tr_item.find("a").get_text())
        tr_item_all = tr_item.findAll("td")
        as_list_item.append(tr_item_all[1].get_text())
        as_list_item.append(locale.atoi(tr_item_all[2].get_text()))
        as_list_item.append(locale.atoi(tr_item_all[3].get_text()))
        as_page_url = "https://whois.ipip.net" + tr_item.find("a").attrs['href']
        as_list_item.append(as_page_url)
        as_list.append(as_list_item)
        as_list_item = []
        rank_cnt += 1
    # 把获取到的AS list写入到文件中
    # print(as_list)
    page_url_copy = page_url
    as_country = page_url_copy.split("/")[-1]
    # print(page_url_copy)
    save_path = "./data/countries_asns_" + as_country + ".csv"
    write_to_csv(as_list, save_path)

    # 2.获取每个ASNs的详细信息，结合CAIDA的BGP互联关系数据进行分析
    temp_list = ["AS Number", "All Relationships", "Peer", "Transit", "Transit(as Provider)", "Transit(as Customer)"]
    print(temp_list)
    result_list.append(temp_list)
    temp_list = []
    for item in as_list[1:]:
        as_number = item[1]
        print(as_number)
        temp_list.append(as_number)
        analysis_result = as_rank_cn(as_number[2:])
        temp_list.append(analysis_result[0])
        temp_list.append(analysis_result[1])
        temp_list.append(analysis_result[2])
        temp_list.append(analysis_result[3])
        temp_list.append(analysis_result[4])
        print(temp_list)
        result_list.append(temp_list)
        temp_list = []
    # 存储as_analysis_cn
    save_path = "./data/as_analysis_cn.csv"
    write_to_csv(result_list, save_path)


def as_rank_cn(as_n):
    """
    根据传入的ASN，结合CAIDA的BGP互联数据进行分析
    :param as_n:
    :return:
    """
    # print(as_n)
    as_rel_file = "./data/20191001.as-rel.txt"

    file_read = open(as_rel_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_provider_cnt = 0
    transit_customer_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[0] == as_n:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

        if line.strip().split('|')[1] == as_n:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1
    return edge_cnt, peer_cnt, transit_provider_cnt + transit_customer_cnt, transit_provider_cnt, transit_customer_cnt


if __name__ == "__main__":
    web_url = "https://whois.ipip.net/countries/CN"  # 入口地址
    time_start = time.time()
    # 启动浏览器
    driver = webdriver.Firefox()
    try:
        obtain_country_asns(web_url)
    except Exception as e:
        print(e)
    # 关闭浏览器
    driver.quit()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")
