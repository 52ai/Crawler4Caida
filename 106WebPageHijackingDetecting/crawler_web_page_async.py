# coding:utf-8
"""

create on Jul. 6, 2023 By Wayne YU
Email: ieeflsyu@outlook.com


Function:

一、整体需求
1、遍历国内网站列表，捕获网站首页截图、提取页面关键词（即指纹），存档。
2、每隔一段时间，重新抓取，并匹配，判断该网站是否存在网页劫持篡改的情况（需剔除其他原因，如网站故障、页面更新等）


二、已有基础
1、10million domains
2、IPIP地理定位库

三、整体思路
1、通过域名解析(socket、ipwhois、python-whois)，拿到网站的IP地址，然后通过IPIP地理定位(ipip-ipdb)，判断其是否为国内，同时看看时延情况如何；
2、对于国内的域名，抓取其首页截图(playwright)、提取页面关键词（即指纹），然后存档；
3、每隔1天，重新抓取，然后逐一判断是否被劫持篡改。

按照上述思路，先出一个MVP（Minimum Viable Product）

# 20230714 采用并发或异步提高爬取效率

"""

import socket
# from ping3 import ping
from ipdb import City
import time
import whois
import tldextract
import csv
from playwright.sync_api import sync_playwright
import os
from urllib.parse import urlparse


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_cn_domains():
    """
    读取10million域名信息，获取中国域名
    亦可通过whois 域名信息，或者自行爬取，然后判断页面内容是否为中文，方法可以多样
    将国内域名获取进行解耦，先形成简单可用的系统，交付给领导
    :return:
    """
    top_10_million_domains_file = "../000LocalData/Domains/top10milliondomains.csv"
    db = City("../000LocalData/ipdb/caict_ipv4.ipdb")
    print("构建IPIP地理定位数据库库（ipdb.build.time）：", db.build_time())

    print("mryu.top whois country:", whois.whois("mryu.top")["country"])
    print("mryu.top host ip:", socket.gethostbyname("mryu.top"))
    print("mryu.top host ip Location Info:", db.find(socket.gethostbyname("mryu.top"), "CN"))

    cn_result_list = []
    with open(top_10_million_domains_file, 'r', encoding='gbk') as f:
        line_cnt = 0
        for line in f.readlines()[1:]:
            line_cnt += 1  # 统计行数
            line = line.replace('"', "")  # 替换掉字符串中的双引号
            line = line.strip().split(",")
            url_format = tldextract.extract(line[1])
            if url_format.suffix.find("cn") != -1:
                print(line)
                # print(url_format.suffix)
                cn_result_list.append([line[1]])
    save_file = "../000LocalData/106WebPage/cn_domains.csv"
    write_to_csv(cn_result_list, save_file)


def gain_website_info():
    """
    根据初版的国内域名列表，逐行抓取网站首页截图及页面内容指纹
    按日期建立文件夹，每日生成快照
    启动匹配程序本质上是匹配不同日期文件夹中的相同网站的截图和页面信息的具体情况（可以用到一些朴素匹配或机器学习模型）
    :return:
    """
    cn_domains_file = "../000LocalData/106WebPage/cn_domains_test.csv"

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        # 打开国内域名列表文件
        with open(cn_domains_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                print("------------------------")
                line = line.strip().split(",")
                page_url = "http://" + line[0]
                print(page_url)
                time_format_date = "%Y%m%d"
                time_date_str = time.strftime(time_format_date, time.localtime())
                data_dir = "../000LocalData/106WebPage/" + time_date_str
                if not os.path.exists(data_dir):
                    os.makedirs(data_dir)
                    print("Create Directory:", data_dir)

                domain_name = urlparse(page_url).netloc.strip("www.")
                site_str = domain_name.replace(".", "_")
                save_path_png = data_dir + "/" + site_str + "_" + time.strftime(time_format_date, time.localtime()) + ".png"
                save_path_html = data_dir + "/" + site_str + "_" + time.strftime(time_format_date, time.localtime()) + ".html"

                # print("png path:", save_path_png)
                # print("html path:", save_path_html)

                if os.path.exists(save_path_png):
                    print("Already Crawler, Next!")
                    continue
                try:
                    page.goto(page_url)
                    page.wait_for_load_state("load")
                    page.screenshot(path=save_path_png)
                    page_html = page.content()
                    with open(save_path_html, "w", encoding="utf-8") as f_html:
                        f_html.write(page_html)
                except Exception as e:
                    print(e)
                    print("!!!!!!!!!!!!!!!!!!!!!!!!")


if __name__ == '__main__':
    time_start = time.time()
    time_format = "%Y%m%d %H:%M:%S"
    time_str = time.strftime(time_format, time.localtime())
    print("=======>启动国内域名首页截屏及关键词提取任务：", time_str)
    # gain_cn_domains()
    gain_website_info()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
