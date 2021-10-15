# coding: utf-8
"""
create on Oct 14, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

本程序是为了爬取TLDs信息，页面连接为https://www.iana.org/domains/root/db
爬取字段为DOMAIN、TYPE、TLD MANAGER
以及详细页面的NAME SERVERS IP
并将NAME SERVERS IP反查其NAME SERVERS AS

iana网站做了防爬措施，频繁访问会禁IP地址，可以转换思路，用whois接口实现

"""

import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import ipinfo


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s> .." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def obtain_ns_ip(page_url):
    """
    根据TLDs详细页面的信息，提取name servers的ip地址信息
    :param page_url:
    :return ns_ip_list:
    """
    ns_ip_list = []  # 存储name servers的ip地址信息
    driver.get(page_url)
    time.sleep(2)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面html信息
    page_html = driver.page_source
    bs_obj = BeautifulSoup(page_html, "html.parser")
    tr_list = bs_obj.find("table").find("tbody").findAll("tr")
    for tr_item in tr_list:
        tr_item_all = tr_item.findAll("td")
        ip_list = str(tr_item_all[1]).strip("<td>").strip("</td>").rstrip("<br/>").split("<br/>")
        ns_ip_list.extend(ip_list)
    return ns_ip_list


def obtain_tlds_list(page_url):
    """
    第一步：根据传入的Root Zone Database，爬取tlds信息
    :param page_url:
    :return tlds_list:
    """
    tlds_list = []  # 存储tlds信息
    driver.get(page_url)
    time.sleep(0.1)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    bs_obj = BeautifulSoup(page_html, "html.parser")
    # print(bs_obj)

    tr_list = bs_obj.find("table").find("tbody").findAll("tr")
    print("TLDs记录数量：", len(tr_list))
    for tr_item in tr_list:
        # print(tr_item)

        tr_item_all = tr_item.findAll("td")
        tld_name = tr_item_all[0].find("a").get_text()
        tld_detail_url = "https://www.iana.org" + tr_item_all[0].find("a").attrs['href']
        tld_type = tr_item_all[1].get_text()
        tld_manager = str(tr_item_all[2].get_text())
        tld_manager = tld_manager.replace(".", "")
        tld_manager = tld_manager.replace(",", " ")
        tld_manager = tld_manager.strip()

        if tld_manager.find("Not assigned") != -1 \
                or tld_manager.find("Retired") != -1 \
                or tld_manager.find("Internet Assigned Numbers Authority") != -1:
            # 该TLD未分配，直接略过
            continue
        """
        第二步：根据tld detail url 获取name server ip地址
        """
        ns_ip = ""
        ns_as = ""
        try:
            ns_ip_result = obtain_ns_ip(tld_detail_url)
            ns_ip = ns_ip_result[0]
            print(ns_ip)
            """
            第三步：根据name server ip地址获取TLDs所属AS网络
            """
            access_token = 'ef73cf9eb4ebf9'
            handler = ipinfo.getHandler(access_token)
            details = handler.getDetails(ns_ip_result[0])
            org_info = str(details.org)
            ns_as = org_info.split(" ")[0]
            print(ns_as)

        except Exception as ns_ip_e:
            print("Error： ", ns_ip_e)

            try:
                time.sleep(2)  # 等待2s
                print("Reload...")
                ns_ip_result = obtain_ns_ip(tld_detail_url)
                print(ns_ip_result[0])
                """
                第三步：根据name server ip地址获取TLDs所属AS网络
                """
                access_token = 'ef73cf9eb4ebf9'
                handler = ipinfo.getHandler(access_token)
                details = handler.getDetails(ns_ip_result[0])
                org_info = str(details.org)
                ns_as = org_info.split(" ")[0]
                print(ns_as)
            except Exception as ns_ip_e:
                print("Error Again：", ns_ip_e)

        finally:
            print(tld_name, tld_type, tld_manager, tld_detail_url)
            tlds_list.append([tld_name, tld_type, tld_manager, ns_ip, ns_as])
            with open("tlds_result_rt.csv", "a", newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=",", quotechar='"')
                writer.writerow([tld_name, tld_type, tld_manager, ns_ip, ns_as])

    return tlds_list


if __name__ == "__main__":
    web_url = "https://www.iana.org/domains/root/db"
    time_start = time.time()
    # 启动浏览器
    driver = webdriver.Firefox()
    try:
        tlds_result = obtain_tlds_list(web_url)
        write_to_csv(tlds_result, "tlds_result.csv")
    except Exception as e:
        print(e)

    driver.quit()
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
