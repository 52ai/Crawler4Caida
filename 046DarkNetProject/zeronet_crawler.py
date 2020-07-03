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
import csv


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
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_zerosites_info(sites_url):
    """
    根据传入的sites_url，构建ZeroSites内容爬取程序
    :param sites_url:
    :return zerosites_info_list:
    """
    zerosites_info_list = []  # 存储站点列表信息，category_name, site_url, site_title, site_description
    print("- - - - - - - - - - - - 暗网爬取程序- - - - - - - - - - - - - -")
    print("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("ZeroNet数据爬取入口地址：", sites_url)
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(sites_url)
    time.sleep(1)  # 延迟加载等待页面加载完毕
    driver.switch_to.frame("inner-iframe")
    """
    ZeroSites存在网站动态刷新的问题，因此需要执行JS代码，实现更多的网址加载
    触发show more的JS Click事件
    """
    print("动态刷新网站列表...")
    # show_more_list = driver.find_element_by_class_name("more")
    # while show_more_list:
    #     show_more_list.click()
    #     show_more_list = driver.find_element_by_class_name("more")
    show_more_list = driver.find_elements_by_xpath("//a[@class='more']")
    print("刷新Show More数量：", len(show_more_list))
    while len(show_more_list) > 0:
        for show_more_item in show_more_list:
            show_more_item.click()
        show_more_list = driver.find_elements_by_xpath("//a[@class='more']")
        print("刷新Show More数量：", len(show_more_list))

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
    # 将分类bs object分类存储在列表中
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
                item_star = category_sites_item.find("div", {"class": "right"}).find("a", {"class": "star"}).\
                    find("span", {"class": "num"}).get_text()
                item_peers = category_sites_item.find("div", {"class": "right"}).find("div", {"class": "peers"}).\
                    find("span", {"class": "num"}).get_text()
                print("网站链接:", item_url)
                print("网站名称:", item_title)
                print("网站描述:", item_description)
                print("喜欢数量:", item_star)
                print("对等数量:", item_peers)
                print()
                # 将站点信息存储到列表中
                zerosites_info_list.append([category_name, " " + item_url, " " + item_title, " " + item_description,
                                            " " + item_star, " " + item_peers])
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
                item_star = category_sites_item.find("div", {"class": "right"}).find("a", {"class": "star"}). \
                    find("span", {"class": "num"}).get_text()
                item_peers = category_sites_item.find("div", {"class": "right"}).find("div", {"class": "peers"}). \
                    find("span", {"class": "num"}).get_text()
                print("网站链接:", item_url)
                print("网站名称:", item_title)
                print("网站描述:", item_description)
                print("喜欢数量:", item_star)
                print("对等数量:", item_peers)
                print()
                # 将站点信息存储到列表中
                zerosites_info_list.append([category_name, " " + item_url, " " + item_title, " " + item_description,
                                            " " + item_star, " " + item_peers])

        except Exception as e:
            # print("Tips:无效记录, ", e)
            pass

    # 关闭浏览器
    driver.quit()
    return zerosites_info_list


if __name__ == "__main__":
    zerosites_url = "http://127.0.0.1:43110/Sites.ZeroNetwork.bit/?Home"
    time_start = time.time()  # 记录程序的启动时间
    main_zerosites_info_list = gain_zerosites_info(zerosites_url)
    print("数据爬取结束，共获取%s条记录" % len(main_zerosites_info_list))
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    zerosites_info_save_path = "../000LocalData/darknet/zerosites_info_" + time_str + ".csv"
    write_to_csv(main_zerosites_info_list, zerosites_info_save_path)
    time_end = time.time()  # 记录程序结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "s")
