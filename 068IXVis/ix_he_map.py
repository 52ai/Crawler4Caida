# coding:utf-8
"""
create on Jun 2, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

HE的数据没有交换中心的经纬度信息，好在通过城市和国家，结合Google Map可以拿到IXP的经纬度的信息

"""
import csv
import time
# 实现无可视化界面
from selenium.webdriver.firefox.options import Options
# 实现规避检测
from selenium import webdriver
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
    根据ix he数据，获取经纬度信息
    :return:
    """
    ix_he_file = "./ix_he.CSV"
    file_read = open(ix_he_file, 'r')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        search_key = line[2] + "," + line[3]
        # print(search_key)

        try:
            ix_geo = gain_geo_from_googlemap(search_key)
        except Exception as e:
            print(e)
            ix_geo = []
        print(ix_geo)
        line.extend(ix_geo)
        """
         将每次获取到的经纬度信息，实时写入到文件中，以防止丢失
         """
        with open("ix_he_geo.csv", "a", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"')
            writer.writerow(line)


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


