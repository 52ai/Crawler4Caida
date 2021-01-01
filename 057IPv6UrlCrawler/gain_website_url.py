# coding:utf-8
"""
Create on Dec 31, 2019 By Wayne

程序功能：
获取给定网站的二级链接以及三级链接

"""

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
from urllib import request


def write_to_csv(res_list, des_path, title_list):
    """
    把给定的List，写到指定路径的文件中
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
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_inner_url(page_url):
    """
    根据传入的page_url,构建内链爬取程序
    :param page_url:
    :return inner_url_list:
    """
    inner_url_list = []  # 存储当前页面内列表
    return inner_url_list


def gain_multistage_url(site_url):
    """
    根据传入的site_url,构建多级（二级、三级）链接爬取程序
    :param site_url:
    :return multistage_url_list:
    """
    multistage_url_list = []  # 存储多级链接
    site_url = "http://"+site_url+"/"
    domain_name = urlparse(site_url).netloc.strip("www.")
    print("当前站点地址：", site_url, "域名模式：", domain_name)
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(site_url)
    time.sleep(5)  # 延迟加载，等待页面加载完毕
    page_html = driver.page_source
    # print(page_html)
    bs_obj = BeautifulSoup(page_html, "html5lib")
    site_lists = bs_obj.findAll("a")
    print("处理前二级链接个数:", len(site_lists))
    # print(site_lists)
    stage2url_list_inner = []  # 存储内链链接
    stage2url_list_outer = []  # 存储外部链接及无效链接
    for item in site_lists:
        try:
            url_str = item.attrs['href']
        except Exception as e:
            print("href提取失败:", e)
            continue
        """
        对获取到的原始二级链接做如下处理：
        由于网站页面采用selenium的无头浏览器动态加载完毕，所有资源均为加载完后的静态资源，避免对每个网站的JS代码进行繁琐的分析
        处理逻辑1：仅取页面内的超链
        处理逻辑2："./XXX"以及"/XXXX"的内链，按照入口站点地址主域名进行拼接（注意：在获取三级内链时，需要重定向之后的站点地址）
        处理逻辑3：根据站点的地址，提取主域，按照主域去提取内链。（同时剔除了外链和无效链接）
        """
        if url_str.find("./") == 0:
            # 找到的"./XXXX"形式的内链,按照站点地址进行拼接
            url_str = "http://" + urlparse(site_url).netloc + "/" + url_str.strip().strip("./")
            print(url_str)

        if url_str.find("http") == -1 and url_str.find(":") == -1 and url_str.find("..") == -1:
            if url_str.find("/") == -1:
                # 找到"XXX"形式的内链
                url_str = "http://" + urlparse(site_url).netloc + "/" + url_str.strip()
                print(url_str)
            elif url_str.find("//") == -1:
                # 找到"/XXXX"形式的内链
                url_str = "http://" + urlparse(site_url).netloc + "/" + url_str.strip()[1:]
                print(url_str)
            else:
                # 找到"//XXX"形式的绝对链接
                url_str = "http:" + url_str
                print(url_str)

        if url_str.find(domain_name) != -1:
            # 判断是否为内链，若是则输出
            # print(url_str)
            stage2url_list_inner.append(url_str)
        else:
            stage2url_list_outer.append(url_str)

    print("处理后二级内链数量:", len(stage2url_list_inner))
    print("处理后二级外链及无效链数量:", len(stage2url_list_outer))

    """
    对每个二级内链，先获取其重定向后的url
    然后访问该内链，抓取三级内链，抓取思路类似于二级内链的抓取
    """
    for item in stage2url_list_inner:
        try:
            # 设置最长等待时间
            driver.set_page_load_timeout(2)
            driver.set_script_timeout(2)
            print("当前访问二级链：", item)
            driver.get(item)
            time.sleep(1)  # 延迟加载，等待页面加载完毕
        except Exception as e:
            print("访问二级链超时：", e)
            driver.execute_script('window.stop()')

        try:
            redirect_url = driver.current_url
            print("实际访问二级链：", redirect_url)
            stage2_domain_name = urlparse(redirect_url).netloc.strip("www.")
            print("域名模式：", stage2_domain_name)
            # print(urlparse(redirect_url))
            """
            需要匹配出当前url的绝对目录
            """
            if redirect_url.split("/")[-1].find("."):
                abs_dir = redirect_url[0:redirect_url.rfind("/")]
            else:
                abs_dir = redirect_url
            print("当前绝对目录:", abs_dir)

            page_html = driver.page_source
            bs_obj = BeautifulSoup(page_html, "html5lib")
            site_lists = bs_obj.findAll("a")
            print("处理前三级连接个数:", len(site_lists))
            stage3url_list_inner = []  # 存储内链链接
            stage3url_list_outer = []  # 存储外部链接及无效链接
            for item_url in site_lists:
                try:
                    url_str = item_url.attrs['href']
                except Exception as e:
                    print("href提取失败:", e)
                    continue
                if url_str.find("./") == 0:
                    # 找到的"./XXXX"形式的内链,按照站点地址进行拼接
                    url_str = abs_dir + "/" + url_str.strip().strip("./")
                    print(url_str)

                if url_str.find("http") == -1 and url_str.find(":") == -1 and url_str.find("..") == -1:
                    if url_str.find("/") == -1:
                        # 找到"XXXX"形式的内链
                        url_str = abs_dir + "/" + url_str.strip()
                        print(url_str)
                    elif url_str.find("//") == -1:
                        # 找到"/XXXX"形式的内链
                        url_str = "http://" + urlparse(redirect_url).netloc + "/" + url_str.strip()[1:]
                        print(url_str)
                    else:
                        # 找到"//XXX"形式的绝对链接
                        url_str = "http:" + url_str
                        print(url_str)

                if url_str.find(domain_name) != -1:
                    # 判断是否为内链，若是则输出
                    # print(url_str)
                    stage3url_list_inner.append(url_str)
                else:
                    stage3url_list_outer.append(url_str)
            print("处理后三级内链数量:", len(stage3url_list_inner))
            print("处理后三级外链及无效链数量:", len(stage3url_list_outer))
            """
            将最后的结果存到multistage_url_list中
            """
            for item_url in stage3url_list_inner:
                multistage_url_list.append([item, item_url])

        except Exception as e:
            print("内链提取失败:", e)

    # 关闭浏览器
    driver.quit()
    return multistage_url_list


if __name__ == "__main__":
    # site_list = ["www.cq.gov.cn"]
    """
    读取网站列表
    """
    fail_log = []  # 存储失败日志
    site_list = []  # 存储读取的网站列表
    sites_file = "../000LocalData/IPv6UrlCrawler/cqsites_v2"
    file_in = open(sites_file, "r", encoding="utf-8")
    for line in file_in.readlines():
        site_list.append(line.strip())
    print("待抓取的网站数量:", len(site_list))

    time_start = time.time()  # 记录程序的启动时间
    print("- - - - - - - - - - - - 站点内链爬取程序- - - - - - - - - - - - - -")
    print("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    for site_item in site_list:
        result_url_list = []
        try:
            result_url_list = gain_multistage_url(site_item)
        except Exception as e:
            print("站点链接抓取失败，", e)
            fail_log.append(["站点链接抓取失败，", e])

        if len(result_url_list) == 0:
            try:
                result_url_list = gain_multistage_url(site_item)
            except Exception as e:
                print("站点链接抓取失败，", e)
                fail_log.append(["站点链接抓取失败，", e])
        # print(result_url_list)
        site_item_str = site_item.replace(".", "")
        save_path = "../000LocalData/IPv6UrlCrawler/" + site_item_str + ".csv"
        write_to_csv(result_url_list, save_path, ["stage2link", "stage3link"])
    print("Fail Log:", fail_log)
    time_end = time.time()  # 记录程序的结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
