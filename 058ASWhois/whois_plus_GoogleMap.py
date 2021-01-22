# coding: utf-8
"""
create on Jan 20, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据AS的whois信息，结合Google Map获取经纬度信息

"""
import csv
import time
# 实现无可视化界面
from selenium.webdriver.firefox.options import Options
# 实现规避检测
from selenium.webdriver import FirefoxOptions

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


def gain_geo_from_googlemap(desrc_str):
    """
    根据desrc_str从Google Map中获取经纬度信息
    :param desrc_str:
    :return geo:
    """
    # 设置最长等待时间
    driver.set_page_load_timeout(8)
    driver.set_script_timeout(8)
    geo = []  # 存储经纬度信息
    site_url = "https://www.google.com.hk/maps/"
    driver.get(site_url)
    input_element = driver.find_element_by_id("searchboxinput")
    input_element.send_keys(desrc_str)
    input_element.submit()
    time.sleep(1)
    submit_btn = driver.find_element_by_id("searchbox-searchbutton")
    submit_btn.click()
    time.sleep(3)
    current_url = driver.current_url
    # if current_url.find("/place/") != -1:
    patt = re.compile(r'[@].+[/]')
    geo_str = " ".join(patt.findall(current_url))
    geo_str = geo_str.strip().strip("@").split(",")
    if len(geo_str) == 3:
        # print(geo_str[0], geo_str[1])
        geo.append(geo_str[0])  # 维度
        geo.append(geo_str[1])  # 经度
    print(current_url)
    return geo


def gain_geo():
    """
    根据AS Whois信息，获取经纬度信息
    """
    country2str = gain_countryinfo()  # 获取国家全称
    # print(country2str)
    result_list = []  # 存储结果列表
    as_info_file = 'D:/Code/Crawler4Caida/000LocalData/as_Gao/asn_info_copy.txt'
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as_desrc = line[1].strip().split(",")[0:-1]
        as_desrc = ' '.join(as_desrc)
        as_desrc = as_desrc.strip()
        try:
            as_desrc_key = as_desrc.split(" - ")[-1] + "," + country2str[as_country]
        except Exception as e:
            print(e)
            as_desrc_key = as_desrc.split(" - ")[-1] + "," + as_country
        # print(as_number, as_desrc, as_country)
        # print(as_number, as_desrc_key)
        try:
            as_geo = gain_geo_from_googlemap(as_desrc_key)
        except Exception as e:
            print(e)
            as_geo = []
        # print(as_number, as_geo)
        print("AS", as_number, as_desrc, as_country, as_geo)
        temp_line = [as_number, as_desrc, as_country]
        temp_line.extend(as_geo)
        result_list.append(temp_line)
        """
        将每次获取到的经纬度信息，实时写入到文件中，以防止丢失
        """
        with open("D:/Code/Crawler4Caida/058ASWhois/asns_google.csv", "a", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            writer.writerow(temp_line)

    # save_path = "D:/Code/Crawler4Caida/058ASWhois/asns_google.csv"
    # write_to_csv(result_list, save_path, ["# Whois Google Geo"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    # 实现无可视化界面
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--disable-gpu')
    # 启动浏览器
    driver = webdriver.Firefox(options=firefox_options)
    # driver = webdriver.Firefox()
    driver.maximize_window()
    site_url = "https://www.google.com.hk/maps/"
    driver.get(site_url)
    gain_geo()
    # 关闭浏览器
    driver.quit()
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")