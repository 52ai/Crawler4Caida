# coding:utf-8
"""
create on July 1, 2020 by Wenyan YU
Function:

暗网的研究，从技术上而言是没有问题的，但是从内容上而言却有一定风险
奈何部门有相关项目，本程序不过多谈论暗网的内容
仅仅从技术层面上开展研究

一般而言，暗网包含Tor、I2P、ZeroNet三块内容
Tor暗网用洋葱路由组成匿名网络
I2P暗网用打算路由组成匿名网络
ZeroNet暗网其实是一个区块链落地应用，使用Bitcoin+BitTorrent技术本身不具备匿名，但可通过Tor来匿名

本程序主要实现对ZeroNet进行简单的数据探测分析

"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup


def gain_zerosites_info(sites_url):
    """
    根据传入的sites_url，构建ZeroSites内容爬取程序
    :param sites_url:
    :return:
    """
    print("- - - - - - - - - - - - 暗网爬取程序- - - - - - - - - - - - - -")
    print("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("ZeroNet数据爬取入口地址：", sites_url)
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(sites_url)
    time.sleep(1)  # 延迟加载等待页面加载完毕
    driver.switch_to.frame("inner-iframe")
    page_html = driver.page_source
    # print(page_html)
    bs_obj = BeautifulSoup(page_html, "html.parser")
    site_lists = bs_obj.find("div", {"class": "sitelists"})
    print("ZeroNet数据分类爬取：", len(site_lists))
    category_list = []  # 存储分类的bs对象
    for site_list in site_lists:
        # print(site_list)
        category_name = site_list.find("a").get_text()
        print(category_name)
        category_list.append(site_list)
    # 将分类bs object分类存储在列表中，针对每一个分类进行爬取（需要动态触发JS实现更多网址的加载）
    # 爬取出Other外的分类
    for category_item in category_list[0:-1]:
        category_name = category_item.find("a").get_text()
        print("- - - - - - -开始爬取分类%s- - - - - - - - - " % category_name)
        category_sites = category_item.find("div", {"class": "sites"})
        for category_sites_item in category_sites:
            try:
                item_url = "http://127.0.0.1:43110" + category_sites_item["href"]
                item_title = category_sites_item.find("div", {"class": "title"}).get_text()
                item_description = category_sites_item.find("div", {"class": "description"}).get_text()
                print("网站链接:", item_url)
                print("网站名称:", item_title)
                print("网站描述:", item_description)
                print()
            except Exception as e:
                pass

    # 爬取Other分类
    category_item = category_list[-1]
    # print(len(category_item))
    category_name = category_item.find("a").get_text()
    print("- - - - - - -开始爬取分类%s- - - - - - - - - " % category_name)
    for category_item_col in category_item:
        try:
            category_sites = category_item_col.find("div", {"class": "sites"})
            for category_sites_item in category_sites:
                item_url = "http://127.0.0.1:43110" + category_sites_item["href"]
                item_title = category_sites_item.find("div", {"class": "title"}).get_text()
                item_description = category_sites_item.find("div", {"class": "description"}).get_text()
                print("网站链接:", item_url)
                print("网站名称:", item_title)
                print("网站描述:", item_description)
                print()

        except Exception as e:
            # print("Tips:无效记录, ", e)
            pass

    # 关闭浏览器
    driver.quit()


if __name__ == "__main__":
    zerosites_url = "http://127.0.0.1:43110/Sites.ZeroNetwork.bit/?Home"
    time_start = time.time()  # 记录程序的启动时间
    gain_zerosites_info(zerosites_url)
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "s")
