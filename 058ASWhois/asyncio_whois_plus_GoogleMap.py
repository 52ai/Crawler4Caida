# coding:utf-8
"""
create on Jan 21, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

综合asns.csv文件，结合Google Map，采用异步网络爬虫技术获取经纬度信息

"""

import csv
import time
# 实现无可视化界面
from selenium.webdriver.firefox.options import Options
# 实现规避检测
from selenium.webdriver import FirefoxOptions

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


from bs4 import BeautifulSoup
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor

org2geo = {}  # 构建机构到Geo的字典
cocurrency = 4  #  最大并发


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None:
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(title_list)
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def gain_countryinfo():
    """
    根据Geo-Country-Locations-en.csv，获取国家全称
    """
    country2str = {}
    country_file = "D:/Code/Crawler4Caida/000LocalData/as_geo/GeoLite2-Country-Locations-en.csv"
    with open(country_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split(",")
            country = line[4]
            country_str = line[5].strip('"')
            country2str[country] = country_str
    return country2str


def gain_geo_from_googlemap(desrc_str, key, driver):
    """
    根据desrc_str从Google Map中获取经纬度信息
    :param desrc_str:
    :return geo:
    """
    # 设置最长等待时间
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    geo = []  # 存储经纬度信息
    site_url = "https://www.google.com.hk/maps/"
    driver.get(site_url)
    input_element = driver.find_element_by_id("searchboxinput")
    input_element.send_keys(desrc_str)
    input_element.submit()
    time.sleep(0.001)
    submit_btn = driver.find_element_by_id("searchbox-searchbutton")
    submit_btn.click()
    time.sleep(5)
    current_url = driver.current_url
    # if current_url.find("/place/") != -1:
    patt = re.compile(r'[@].+[/]')
    geo_str = " ".join(patt.findall(current_url))
    geo_str = geo_str.strip().strip("@").split(",")
    if len(geo_str) == 3:
        # print(geo_str[0], geo_str[1])
        geo.append(geo_str[1])  # 经度
        geo.append(geo_str[0])  # 维度
    org2geo[key] = geo
    print(current_url)
    log_line = []
    log_line.append(key)
    log_line.extend(geo)
    with open("D:/Code/Crawler4Caida/058ASWhois/asyncio_log_redo.csv", "a", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(log_line) 


def do(job_list):
    """
    分组打开浏览器进行抓取
    """
     # 实现无可视化界面
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    # 启动浏览器
    my_driver = webdriver.Firefox(options=firefox_options)
    # my_driver = webdriver.Firefox()
    my_driver.maximize_window()
    site_url = "https://www.google.com.hk/maps/"
    my_driver.get(site_url)
    for job in job_list:
        # print(job[0], job[1])
        try:
            gain_geo_from_googlemap(job[0], job[1], my_driver)
        except Exception as e:
            print("Driver ERROR:", e)
    # 关闭浏览器
    my_driver.quit()


def gain_geo():
    """
    根据AS Whois信息，获取经纬度信息
    """
    country2str = gain_countryinfo()  # 获取国家全称
    as_info_file = 'D:/Code/Crawler4Caida/058ASWhois/asns_copy.csv'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    """
    为方便每一次，尽量减少重复爬取，每次都需读取asyncio_log.csv
    剔除已经抓取的记录
    """
    # 读asyncio log
    done_geo_file = 'D:/Code/Crawler4Caida/058ASWhois/asyncio_log.csv'
    done_org_list = []  # 存储已经抓取的org_list 
    with open(done_geo_file, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            if len(line) == 3:
                done_org_list.append(line)

    # 写asyncio log redo
    done_geo_file_redo = 'D:/Code/Crawler4Caida/058ASWhois/asyncio_log_redo.csv'
    with open(done_geo_file_redo, "a", newline='', encoding='utf-8') as f:
        for line in done_org_list:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(line)
    
    # 读asyncio log redo
    done_geo_file_redo = 'D:/Code/Crawler4Caida/058ASWhois/asyncio_log_redo.csv'
    done_org_list_redo = []  # 存储已经抓取的org_list 
    with open(done_geo_file_redo, 'r', encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            done_org_list_redo.append(line[0])

    print("已抓取机构信息总记录数:", len(done_org_list_redo))
    done_org_list = list(set(done_org_list_redo))
    print("去重之后的机构信息总记录数", len(done_org_list_redo))

    org_list = []  # 存储org信息
    for line in file_read.readlines():
        if line.startswith("#"):
            continue
        line = line.strip().split(",")
        # print(line)
        if len(line) > 3 or line[1].find("Reserved AS") != -1:
            pass
        else:
            as_desrc = line[1]
            org_name = as_desrc.split(" - ")[-1]
            as_country = line[2]
            dict_key = org_name + " - " + as_country
            if dict_key not in done_org_list:
                org_list.append(dict_key)
                
    print("全部机构记录数(需统计)：", len(org_list))
    print("去重之后的机构记录数:", len(list(set(org_list))))

    # print(org2geo)
    org_list = list(set(org_list))
    # with open("D:/Code/Crawler4Caida/058ASWhois/asyncio_org.csv", "a", newline='', encoding='utf-8') as csv_file:
    #     for org_item in org_list:
    #         writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    #         writer.writerow([org_item])
    

    for item in org_list:
        org2geo[item] = []

    max_group_cnt = len(org_list) / cocurrency

    group_list = []  # 用二维数组存储任务分组
    item_cnt = 0
    temp_list = []
    for item in org_list:
        # print(item)
        key_arg = item 
        key = item.strip().split(" - ")
        try:
            org_name = key[0]
            country = key[1].strip("- ")
        except Exception as e:
            print("Split ERROR:", key, e)
            continue

        try:
            desrc_key_str = org_name + ", " + country2str[country]
        except Exception as e:
            print("Country2str ERROR:", key, e)
            desrc_key_str = org_name + ", " + country
        temp_list.append([desrc_key_str, key_arg])
        item_cnt += 1
        if item_cnt > max_group_cnt:
            group_list.append(temp_list)
            temp_list = []
            item_cnt =0
        
    if len(temp_list) != 0:
        group_list.append(temp_list)  # 末尾不足分组的内容

    """
    按组分配任务，各组间异步执行
    """
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(cocurrency)
    tasks = []

    # print(group_list)
    for group_item in group_list:
        print(len(group_item))
        task = loop.run_in_executor(executor, do, group_item)
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))
    

if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    gain_geo()
    print("org LEN:", len(org2geo.keys()))
    for key in org2geo.keys():
        temp_line = []
        temp_line.append(key)
        temp_line.extend(org2geo[key])
        with open("D:/Code/Crawler4Caida/058ASWhois/asyncio_asns_google_all.csv", "a", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            writer.writerow(temp_line)
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")