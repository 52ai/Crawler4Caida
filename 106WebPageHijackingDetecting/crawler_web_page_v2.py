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

# 20230715 为提供页面的抓取速度，使用并发，最佳拍档是selenium

"""
import random
import time
import os
from urllib.parse import urlparse
import threading
from selenium import webdriver


def run_page_list_info_gain_selenium(run_page_list):
    """
    根据传入的page list，多线程爬取页面信息
    :param run_page_list:
    :return:
    """
    # 启动浏览器
    options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")  # 设置火狐为headless无界面模式
    # options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(30)
    # driver.implicitly_wait(15)  # 设置隐性等待时间
    # driver.set_script_timeout(10)
    driver.set_window_size(width=1280, height=720)
    # driver.maximize_window()  # 最大化窗口
    # 遍历传入的page url list
    for run_page in run_page_list:
        # time_format_date = "%Y%m%d"
        # time_date_str = time.strftime(time_format_date, time.localtime())
        # data_dir = "../000LocalData/106WebPage/" + time_date_str
        data_dir = "../000LocalData/106WebPage/20230715_origin"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("Create Directory:", data_dir)

        domain_name = urlparse(run_page).netloc
        site_str = domain_name.replace(".", "_")
        save_path_png = data_dir + "/" + site_str + ".png"
        save_path_html = data_dir + "/" + site_str + ".html"

        print(save_path_png)
        print(save_path_html)

        if os.path.exists(save_path_png):
            print("Already Crawler, Next!")
            continue

        try:
            print("------------------------")
            print(run_page)
            driver.get(run_page)
            # time.sleep(1)  # 强制等待1s
            # 获取网站截图，并保存到本地
            driver.save_screenshot(save_path_png)
            page_html = driver.page_source
            with open(save_path_html, "w", encoding="utf-8") as f_html:
                f_html.write(page_html)
        except Exception as e:
            print(e)
            print("!!!!!!!!!!!!!!!!!!!!!")
            if str(e).find("without establishing a connection") != -1:
                print("连接关闭！！！刷新下浏览器")
                driver.refresh()  # 刷新的浏览器
    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    time_start = time.time()
    time_format = "%Y%m%d %H:%M:%S"
    time_str = time.strftime(time_format, time.localtime())
    print("=======>启动国内域名首页截屏及关键词提取任务：", time_str)

    """
    第一步，获取待爬取的列表，并按照并发线程数将其拆分为不同分任务列表
    """
    page_list_all = []  # 原始page url 列表
    page_list_already = []  # 存储已经抓取的列表
    page_list_group = []  # 分组page url
    n_threading = 3  # 设置并发线程数

    cn_domains_file = "../000LocalData/106WebPage/cn_domains_test.csv"
    with open(cn_domains_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            page_url = "http://" + line[0]

            # time_format_date_out = "%Y%m%d"
            # time_date_str_out = time.strftime(time_format_date_out, time.localtime())
            # data_dir_out = "../000LocalData/106WebPage/" + time_date_str_out
            data_dir_out = "../000LocalData/106WebPage/20230715_origin"
            if not os.path.exists(data_dir_out):
                os.makedirs(data_dir_out)
                print("Create Directory:", data_dir_out)

            domain_name_out = urlparse(page_url).netloc
            site_str_out = domain_name_out.replace(".", "_")
            save_path_png_out = data_dir_out + "/" + site_str_out + ".png"
            save_path_html_out = data_dir_out + "/" + site_str_out + ".html"

            if os.path.exists(save_path_png_out) and os.path.exists(save_path_html_out):
                page_list_already.append(page_url)
            else:
                page_list_all.append(page_url)

    max_page_cnt = (len(page_list_all) // n_threading) + 1  # 向上取整
    print("page list already:", len(page_list_already))
    """
    确定一个可行的最小test group，每天对其进行抓取，比如先确定一个TOP1000的list
    """
    # with open("../000LocalData/106WebPage/cn_domains_day.csv", "w", encoding="utf-8") as f:
    #     for item in page_list_already[0:100]:
    #         f.writelines(item.strip("http://")+"\n")

    print("page list all:", len(page_list_all))
    print("threading:", n_threading)
    print("max_page_cnt:", max_page_cnt)

    random.shuffle(page_list_all)
    temp_list = []  # 存储page list
    page_cnt = 1
    for item_url in page_list_all:
        temp_list.append(item_url)
        if page_cnt == max_page_cnt:
            page_list_group.append(temp_list)
            page_cnt = 0
            temp_list = []
        page_cnt += 1
    page_list_group.append(temp_list)

    print("page url group cnt:", len(page_list_group))
    print(page_list_group)
    """
    第二步：将分组后的任务列表，分给不同的线程独立执行
    """
    threads = []  # 存储线程
    for group_list in page_list_group:
        threads.append(threading.Thread(target=run_page_list_info_gain_selenium, args=(group_list,)))
    for t in threads:
        t.setDaemon(True)
        t.start()

    # 必须等待for循环里面所有的线程都结束，再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
