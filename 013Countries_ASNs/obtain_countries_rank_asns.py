# coding:utf-8
"""
create on Oct 10,2019 by Wayne

Fun:获取全球各个国家的ASNs分配的数量、通告的数量以及ASN V4/V6地址的数量<数据来源：https://whois.ipip.net/countries>

"""
from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
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


def obtain_info(page_url):
    """
    获取Countries ASNs页面的信息，并处理
    :param page_url:
    :return: countries_asns_list
    """
    driver.get(page_url)
    time.sleep(3)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    # print(page_html)
    bsObj = BeautifulSoup(page_html, "html.parser")
    # print(bsObj)

    """
    tr_list = bsObj.find("table",{"class":"table companyInfo-table"}).find("tbody").findAll("tr")
    for tr_item in tr_list:
        shareholer_info =[]
        shareholer_info.append(tr_item.find("a").get_text())
        shareholer_info.append(tr_item.findAll("span")[0].get_text())
        shareholer_info.append(tr_item.findAll("span")[1].get_text())
        shareholer_info_list.append(shareholer_info)
    """
    countries_asns_list = []  # 存储各个国家ASN号的信息，包括Allocated ASNs、Announced ASNs、ASN IPv4 Number、ASN IPv6 Number。
    countries_asns_info = []
    countries_asns_info.append("Rank")
    countries_asns_info.append("Country&Region")
    countries_asns_info.append("Allocated ASNs")
    countries_asns_info.append("Announced ASNs")
    countries_asns_info.append("ASN IPv4 Number")
    countries_asns_info.append("ASN IPv6 Number(/64)")
    countries_asns_info.append("CountryPageUrl")
    countries_asns_list.append(countries_asns_info)
    countries_asns_info = []
    rank_cnt = 1
    tr_list = bsObj.find("table").find("tbody").findAll("tr")
    for tr_item in tr_list:
        # print(item)
        countries_asns_info.append(rank_cnt)
        countries_asns_info.append(tr_item.find("a").get_text())
        tr_item_all = tr_item.findAll("td")
        countries_asns_info.append(locale.atoi(tr_item_all[1].get_text()))
        countries_asns_info.append(locale.atoi(tr_item_all[2].get_text()))
        countries_asns_info.append(locale.atoi(tr_item_all[3].get_text()))
        countries_asns_info.append(locale.atoi(tr_item_all[4].get_text()))
        country_page_url = "https://whois.ipip.net" + tr_item.find("a").attrs['href']
        countries_asns_info.append(country_page_url)
        countries_asns_list.append(countries_asns_info)
        countries_asns_info = []
        rank_cnt += 1
    # print(countries_asns_list)
    return countries_asns_list


def obtain_country_asns(page_url):
    """
    根据每个国家的ASNs网页信息，抓取每个国家已经分配的ASNs信息及AS号的IP地址范围（IPv4和IPv6）、上游、下游、与交换中心的连接情况、托管域、whois
    :param page_url:
    :return None:
    """
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

    # 2.获取每个ASNs的详细信息
    # 循环读取，AS list每一个as_page_url，通过浏览器访问该页面，并按格式获取该页面信息
    # as_page_url_next = "https://whois.ipip.net/AS4134"
    # obtain_as_info(as_page_url_next, as_country)

    for item in as_list[1:]:
        as_page_url_next = item[-1]
        # print(as_page_url_next)
        obtain_as_info(as_page_url_next, as_country)


def obtain_as_info(page_url, as_country):
    """
    根据给定的url，获取该ASNs的详细信息
    需要注意的是，每个AS的页面的信息不一定很全,有些页面可能只有部分，要做异常处理
    :param page_url:
    :return as_info:
    """
    as_info = []
    as_info_cache = []
    driver.get(page_url)
    time.sleep(3)  # 延迟加载，等待页面的内容加载完毕
    # 获取页面的html信息
    page_html = driver.page_source
    # print(page_html)
    bsObj = BeautifulSoup(page_html, "html.parser")
    # print(bsObj)

    # =============获取该AS号的AS info=================
    td_list = bsObj.find("table", {"class": "table table-bordered"}).findAll("td")
    # print(td_list)
    as_number = page_url.split("/")[-1]
    as_info_cache.append("=>AS INFO: %s" % as_number)
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append("AS Name")
    as_info_cache.append("Org Name")
    as_info_cache.append("IPv4Prefixes")
    as_info_cache.append("IPv6Prefixes")
    as_info_cache.append("IPv4 NUMs")
    as_info_cache.append("IPv6 NUMs")
    as_info_cache.append("Registry Region")
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append(td_list[0].get_text())
    as_info_cache.append(td_list[1].get_text())
    as_info_cache.append(locale.atoi(td_list[2].get_text()))
    as_info_cache.append(locale.atoi(td_list[3].get_text()))
    as_info_cache.append(locale.atoi(td_list[4].get_text()))
    as_info_cache.append(locale.atoi(td_list[5].get_text()))
    as_info_cache.append(td_list[6].find("a").get_text().strip())
    as_info.append(as_info_cache)
    as_info_cache = []

    # 添加一条有态度的分割线
    as_info_cache.append("---------------------------------------")
    as_info.append(as_info_cache)
    as_info_cache = []

    # =========获取IPv4 Ranges============
    # 需做异常处理

    as_info_cache.append("=>IPv4 Ranges")
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append("CIDR")
    as_info_cache.append("Description")
    as_info_cache.append("IP Num")
    as_info.append(as_info_cache)
    as_info_cache = []

    try:
        tr_list = bsObj.find("div", {"id": "pills-ipv4"}).find("tbody").findAll("tr")
        for tr_item in tr_list:
            # print(tr_item)
            td_all = tr_item.findAll("td")
            as_info_cache.append(td_all[0].find("a").get_text())
            as_info_cache.append(td_all[1].get_text())
            as_info_cache.append(td_all[2].get_text())
            as_info.append(as_info_cache)
            as_info_cache = []
    except Exception as e:
        print(e)
    finally:
        # 添加一条有态度的分割线
        as_info_cache.append("---------------------------------------")
        as_info.append(as_info_cache)
        as_info_cache = []

    # ================获取IPv6 Ranges===================
    # 需做异常处理
    # 需要对页面tab进行处理，使用tab的click事件，获取页面信息的更新（不需要）
    # pills_ipv6_tab = driver.find_element_by_id("pills-ipv6-tab")
    # pills_ipv6_tab.click()
    # time.sleep(3)
    # page_html = driver.page_source
    # bsObj = BeautifulSoup(page_html, "html.parser")

    as_info_cache.append("=>IPv6 Ranges")
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append("CIDR")
    as_info_cache.append("Description")
    as_info_cache.append("IP NUMs（prefix/64）")
    as_info.append(as_info_cache)
    as_info_cache = []

    try:
        tr_list = bsObj.find("div", {"id": "pills-ipv6"}).find("tbody").findAll("tr")
        for tr_item in tr_list:
            # print(tr_item)
            td_all = tr_item.findAll("td")
            as_info_cache.append(td_all[0].find("a").get_text())
            as_info_cache.append(td_all[1].get_text())
            as_info_cache.append(td_all[2].get_text())
            as_info.append(as_info_cache)
            as_info_cache = []
    except Exception as e:
        print(e)
    finally:
        # 添加一条有态度的分割线
        as_info_cache.append("---------------------------------------")
        as_info.append(as_info_cache)
        as_info_cache = []

    # ====================获取Upstreams========================
    # 需做异常处理
    as_info_cache.append("=>Upstreams")
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append("Number")
    as_info_cache.append("AS")
    as_info_cache.append("Description")
    as_info_cache.append("Country/Region")
    as_info_cache.append("IPv4 NUMs")
    as_info_cache.append("IPv6 NUMs")
    as_info.append(as_info_cache)
    as_info_cache = []

    try:
        rank_cnt = 1
        tr_list = bsObj.find("div", {"id": "upstream"}).find("tbody").findAll("tr")
        for tr_item in tr_list:
            # print(tr_item)
            as_info_cache.append(rank_cnt)
            td_all = tr_item.findAll("td")
            as_info_cache.append(td_all[0].find("a").get_text())
            as_info_cache.append(td_all[1].get_text())
            as_info_cache.append(td_all[2].find("a").find("img").attrs["src"].split("/")[-1].split('.')[0])
            as_info_cache.append(locale.atoi(td_all[3].get_text()))
            as_info_cache.append(locale.atoi(td_all[4].get_text()))
            as_info.append(as_info_cache)
            as_info_cache = []
            rank_cnt += 1
    except Exception as e:
        print(e)
    finally:
        # 添加一条有态度的分割线
        as_info_cache.append("---------------------------------------")
        as_info.append(as_info_cache)
        as_info_cache = []

    # ====================获取Downstreams========================
    # 需做异常处理
    as_info_cache.append("=>Downstreams")
    as_info.append(as_info_cache)
    as_info_cache = []

    as_info_cache.append("Number")
    as_info_cache.append("AS")
    as_info_cache.append("Description")
    as_info_cache.append("Country/Region")
    as_info_cache.append("IPv4 NUMs")
    as_info_cache.append("IPv6 NUMs")
    as_info.append(as_info_cache)
    as_info_cache = []

    try:
        rank_cnt = 1
        tr_list = bsObj.find("div", {"id": "downstream"}).find("tbody").findAll("tr")
        for tr_item in tr_list:
            # print(tr_item)
            as_info_cache.append(rank_cnt)
            td_all = tr_item.findAll("td")
            as_info_cache.append(td_all[0].find("a").get_text())
            as_info_cache.append(td_all[1].get_text())
            as_info_cache.append(td_all[2].find("a").find("img").attrs["src"].split("/")[-1].split('.')[0])
            as_info_cache.append(locale.atoi(td_all[3].get_text()))
            as_info_cache.append(locale.atoi(td_all[4].get_text()))
            as_info.append(as_info_cache)
            as_info_cache = []
            rank_cnt += 1
    except Exception as e:
        print(e)
    finally:
        # 添加一条有态度的分割线
        as_info_cache.append("---------------------------------------")
        as_info.append(as_info_cache)
        as_info_cache = []

    # =====================获取AS whois==========================
    # 需做异常处理
    as_info_cache.append("=>Whois")
    as_info.append(as_info_cache)
    as_info_cache = []

    try:
        # print(bsObj)
        as_whois = bsObj.find("div", {"id": "whois"}).find("pre").get_text()
        as_info_cache.append(as_whois)
        as_info.append(as_info_cache)
        as_info_cache = []
    except Exception as e:
        print(e)
    finally:
        # 添加一条有态度的分割线
        as_info_cache.append("---------------------------------------")
        as_info.append(as_info_cache)
        as_info_cache = []

    # print(as_info)
    # 把获取到的ASNs信息写道文件中
    save_path = "./data/countries_asns_" + as_country + "_" + as_number + ".csv"
    write_to_csv(as_info, save_path)
    return as_info


if __name__ == "__main__":
    web_url = "https://whois.ipip.net/countries"  # 爬虫的入口地址
    time_start = time.time()
    # 启动浏览器
    # fire_options = Options()
    # fire_options.headless = True
    # driver = webdriver.Firefox(options=fire_options)
    driver = webdriver.Firefox()
    # driver.maximize_window()
    try:
        countries_asns = obtain_info(web_url)
        write_to_csv(countries_asns, "./data/countries_asns.csv")
        # 根据国家ASNs页面地址，获取相关信息
        obtain_country_asns("https://whois.ipip.net/countries/CN")
    except Exception as e:
        print(e)
    # 关闭浏览器
    driver.quit()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")
