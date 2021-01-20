# coding: utf-8
"""
create on Jan 20, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据AS的whois信息，结合Google Map获取经纬度信息

"""
import csv
import time

from selenium import webdriver
from bs4 import BeautifulSoup
import re

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
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        writer.writerow(title_list)
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def gain_geo_from_googlemap(desrc_str):
    """
    根据desrc_str从Google Map中获取经纬度信息
    :param desrc_str:
    :return geo:
    """
    geo = []  # 存储经纬度信息
    site_url = "https://www.google.com.hk/maps/"
    driver.get(site_url)
    input_element = driver.find_element_by_id("searchboxinput")
    input_element.send_keys(desrc_str)
    input_element.submit()
    time.sleep(1)
    submit_btn = driver.find_element_by_id("searchbox-searchbutton")
    submit_btn.click()
    time.sleep(4)
    current_url = driver.current_url
    patt = re.compile(r'[@].+[/]')
    geo_str = " ".join(patt.findall(current_url))
    geo_str = geo_str.strip().strip("@").split(",")
    if len(geo_str) == 3:
        # print(geo_str[0], geo_str[1])
        geo.append(geo_str[0])
        geo.append(geo_str[1])

    print(current_url)
    return geo


def gain_geo():
    """
    根据AS Whois信息，获取经纬度信息
    """
    as_info_file = 'D:/Code/Crawler4Caida/000LocalData/as_Gao/asn_info.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as_desrc = line[1].strip().split(",")[0:-1]
        as_desrc = ' '.join(as_desrc)
        as_desrc = as_desrc.strip()
        as_desrc_key = as_desrc.split(" - ")[-1] + "," + as_country
        print(as_number, as_desrc, as_country)
        print(as_number, as_desrc_key)
        as_geo = gain_geo_from_googlemap(as_desrc_key)
        print(as_number, as_geo)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    gain_geo()
    # 关闭浏览器
    driver.quit()
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")