# coding:utf-8
"""
create on Jan 18, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

抓取BGPStream(https://bgpstream.com/)中安全事件的信息

"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :param title_list:
    :return None:
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
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


def crawler():
    """
    处理页面
    """
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    site_url = "https://bgpstream.com/"
    driver.get(site_url)

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动时间
    crawler()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
