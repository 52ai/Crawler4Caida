# coding:utf-8
"""
create on Sep 3, 2020 By Wenyan YU

Function:

获取RIPE全部25个节点的Message和RIB所有历史数据（直接通过爬虫爬取，省去匹配规则）
由于RIPE网站没有JS防爬措施，直接用requests库即可


在进行直接爬取实验后，时间效率非常之低，仅爬取下载链接就需要好仅两天时间（1个节点2个小时左右）
因此可以尝试使用并行化爬取策略
搞完之后，直接扔给服务器

在完成历史数据的爬取后，可以写个脚本用于实时监控当前最新Update报文MRT文件，便于后面做实时的全球BGP路由监测

"""
from bs4 import BeautifulSoup
import time
import csv
import re
import requests


all_download_link = []  # 存储所有的下载链接


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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_rrc_info(rrc_url):
    """
    根据不同rrc的下载主页，获取全球的下载链接
    :param rrc_url:
    :return:
    """
    print(rrc_url)
    time.sleep(1)  # 延迟加载等待加载完全
    page_html = requests.get(rrc_url)
    bs_obj = BeautifulSoup(page_html.text, "html5lib")
    # print(bs_obj)
    tr_list = bs_obj.find("tbody").findAll("tr")
    month_str_list = []  # 存储所有月份的列表
    for tr_item in tr_list:
        a_item = tr_item.find("a")
        if a_item:
            month_str = a_item.attrs['href']
            if len(re.findall(r"\d+", month_str)) != 0:
                # print(rrc_url+month_str)
                month_str_list.append(rrc_url+month_str)
    # print(month_str_list)

    for month_str_item in month_str_list:
        # print(month_str_item)
        gain_download_list(month_str_item)


def gain_download_list(page_url):
    """
    根据不同的月份文件夹，获取里面所有的Message和RIB下载列表
    :param page_url:
    :return:
    """
    print(page_url)
    page_html = requests.get(page_url)
    bs_obj = BeautifulSoup(page_html.text, "html5lib")
    # print(bs_obj)
    tr_list = bs_obj.find("tbody").findAll("tr")
    url_str_list = []  # 存储所有url的列表
    for tr_item in tr_list:
        a_item = tr_item.find("a")
        if a_item:
            url_str = a_item.attrs['href']
            if url_str.find("gz") != -1:
                url_str_list.append(page_url + url_str)
                all_download_link.append([url_str_list[-1]])  # 保存所有的下载链接
                # print(url_str_list[-1])
    print("当月所有文件记录:", len(url_str_list))
    # print(all_download_link)


if __name__ == "__main__":
    time_start = time.time()
    rrc_list = ["http://data.ris.ripe.net/rrc00/",
                "http://data.ris.ripe.net/rrc01/",
                "http://data.ris.ripe.net/rrc02/",
                "http://data.ris.ripe.net/rrc03/",
                "http://data.ris.ripe.net/rrc04/",
                "http://data.ris.ripe.net/rrc05/",
                "http://data.ris.ripe.net/rrc06/",
                "http://data.ris.ripe.net/rrc07/",
                "http://data.ris.ripe.net/rrc08/",
                "http://data.ris.ripe.net/rrc09/",
                "http://data.ris.ripe.net/rrc10/",
                "http://data.ris.ripe.net/rrc11/",
                "http://data.ris.ripe.net/rrc12/",
                "http://data.ris.ripe.net/rrc13/",
                "http://data.ris.ripe.net/rrc14/",
                "http://data.ris.ripe.net/rrc15/",
                "http://data.ris.ripe.net/rrc16/",
                "http://data.ris.ripe.net/rrc17/",
                "http://data.ris.ripe.net/rrc18/",
                "http://data.ris.ripe.net/rrc19/",
                "http://data.ris.ripe.net/rrc20/",
                "http://data.ris.ripe.net/rrc21/",
                "http://data.ris.ripe.net/rrc22/",
                "http://data.ris.ripe.net/rrc23/",
                "http://data.ris.ripe.net/rrc24/"]
    for item in rrc_list[24:]:
        try:
            gain_rrc_info(item)
        except Exception as e:
            print(e)
    save_path = "all_download_links_ripe.csv"
    write_to_csv(all_download_link, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
