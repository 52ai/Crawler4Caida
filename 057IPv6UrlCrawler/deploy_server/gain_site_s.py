# coding:utf-8
"""
create on Mar 20, 2022 By Wayne YU

程序功能：

近期收到重庆和云南项目需要大量的网站爬取任务，原先基于windows的Firefox图形界面爬取策略已不再胜任
需要在服务器端构建虚拟的图形界面爬取策略

经研究，可将selenium+firefox，替换为playwright+firefox

本程序就是实现这个替换，并尽可能的完善众多网站爬取问题的边界条件，以保证爬虫爬取的准确性、稳定性和健壮性

playwright仅支持Python3.7以上的版本
因此服务器端已安装python3.7，命令识别为python37以及pip37

安装Playwright 1.18.0环境
pip3 install playwright
playwright install

3rd Package
playwright~=1.18.0
beautifulsoup4~=4.9.3
pip37 install beautifulsoup4 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

urllib3~=1.25.11
html5lib~=1.1
"""
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
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


def gain_inner_url(page_url):
    """
    根据传入的page_url,构建内链爬取程序
    :param page_url:
    :return all_url_list:
    :return inner_url_list:
    :return outer_url_list:
    """
    inner_url_list = []  # 存储当前页面内链
    outer_url_list = []  # 存储当前页面外部链接及无效链接
    domain_name = urlparse(page_url).netloc.strip("www.")
    """
    匹配出当前url的绝对目录
    """
    if page_url.split("/")[-1].find("."):
        abs_dir = page_url[0:page_url.rfind("/")]
    else:
        abs_dir = page_url
    print("当前绝对目录:", abs_dir)

    protocol_str = abs_dir.split(":")[0]  # 区分是https协议还是http协议
    # print(protocol_str)

    """
    对获取到的链接做如下处理：
    由于网站页面采用Playwright+Firefox动态加载完毕，所有资源均为加载完后的静态资源，避免对每个网站的JS代码进行繁琐的分析
    处理逻辑1：仅取页面内的超链
    处理逻辑2："./XXXX"、"/XXXXX"、"XXXX/XXXX/"、"//"，按照对应规则进行拼接。（注意：在获取三级内链时，需要重定向之后的站点地址）
    处理逻辑3：根据站点地址，提取主域，按照主域去提取内链。（同时剔除了外链和无效链接）
    """

    page.goto(page_url)
    # time.sleep(3) # 延迟加载，等待页面加载完毕
    page.wait_for_load_state("networkidle")
    page_html = page.content()
    bs_obj = BeautifulSoup(page_html, "html5lib")
    all_url_list = bs_obj.findAll("a")  # 存储全部的原始超链
    all_url_list = list(set(all_url_list))  # 新增去重功能，降低重复链接的爬取时间

    for item in all_url_list:
        try:
            url_str = item.attrs['href']
        except Exception as e_href:
            print("无效a标签:", e_href)
            continue
        """
        处理逻辑
        """
        url_str = url_str.strip()  # 去除前后特殊字符
        url_str = url_str.replace("\\", "/")  # 规范不规则反斜杠
        # print(url_str)

        if url_str.startswith("//"):
            # 找到”//XXX“形式的绝对链接
            url_str = protocol_str + ":" + url_str
            # print(url_str)
        elif url_str.startswith("/"):
            # 找到“/XXXX”形式的绝对路径内链
            url_str = protocol_str + "://" + urlparse(page_url).netloc + url_str
            # print(url_str)
        elif url_str.startswith("./"):
            # 找到“./XXX”形式的相对路径内链
            url_str = abs_dir + "/" + url_str.strip("./")
            # print(url_str)
        elif url_str.find("/") == -1:
            # 找到 "XXXX"形式的相对路径内链
            url_str = abs_dir + "/" + url_str
        elif url_str.find("//") == -1 and url_str.find("/") != -1:
            # 找到 "XXX/XXX/XXX"形式的相对路径内链
            url_str = abs_dir + "/" + url_str

        if url_str.find(domain_name) != -1 and url_str.find("script:") == -1:
            # 判断是否为内链，且不是script脚本，若是则输出
            # print(url_str)
            inner_url_list.append(url_str)
        else:
            outer_url_list.append(url_str)

    return all_url_list, inner_url_list, outer_url_list


def gain_website_url(site_url):
    """
    :param site_url:
    :return multistage_url_list:
    """
    multistage_url_list = []  # 存储多级链接
    page.goto(site_url)
    # time.sleep(3)  # 延迟加载，等待页面跳转结束，解决重定向的问题
    page.wait_for_load_state("networkidle")
    site_url = page.url  # 获取跳转之后的网络链接
    print(site_url)
    domain_name = urlparse(site_url).netloc.strip("www.")
    print("站点地址:", site_url)
    print("域名模式:", domain_name)
    print("- - - - - - - - - - - - 站点二级内链爬取- - - - - - - - - - - - - -")
    site2_lists, stage2url_list_inner, stage2url_list_outer = gain_inner_url(site_url)
    print("处理前二级链接个数:", len(site2_lists))
    print("处理后二级内链数量:", len(stage2url_list_inner))
    print("处理后二级外链及无效链数量:", len(stage2url_list_outer))

    print("- - - - - - - - - - - - 站点三级内链爬取- - - - - - - - - - - - - -")

    """
    对每个二级内链，先获取其重定向后的url
    然后访问该内链，抓取三级内链
    """
    stage2_cnt = 0  # 存储三级连接爬取轮数
    for item in stage2url_list_inner:
        print("\n**%s**" % stage2_cnt)
        stage2_cnt += 1
        try:
            print("当前访问二级链：", item)
            page.goto(item)
            # time.sleep(3)  # 延迟加载，等待二级页面跳转结束，解决重定向的问题
            page.wait_for_load_state("networkidle")
        except Exception as e_stage2:
            print("访问二级链超时：", e_stage2)
            # page.evaluate('window.stop()')

        try:
            redirect_url = page.url
            print("实际访问二级链：", redirect_url)
            stage2_domain_name = urlparse(redirect_url).netloc.strip("www.")
            print("域名模式：", stage2_domain_name)
            site3_lists, stage3url_list_inner, stage3url_list_outer = gain_inner_url(redirect_url)
            print("处理前三级链接个数:", len(site3_lists))
            print("处理后三级内链数量:", len(stage3url_list_inner))
            print("处理后三级外链及无效链数量:", len(stage3url_list_outer))

            """
            将最后的结果存到multistage_url_list中
            """
            for item_url in stage3url_list_inner:
                multistage_url_list.append([item, item_url])
        except Exception as e_stage2:
            print("内链提取失败:", e_stage2)

    return multistage_url_list


def cancel_request(route):
    # print("request:", request)
    route.abort()


if __name__ == "__main__":
    """
    读取网站列表
    """
    fail_log = []  # 存储失败日志
    site_list = []  # 存储读取的网站列表
    sites_file = "site_test"
    file_in = open(sites_file, "r", encoding="utf-8")
    for line in file_in.readlines():
        site_list.append(line.strip())
    print("待抓取的网站数量:", len(site_list))

    time_start = time.time()  # 记录程序的启动时间

    print("- - - - - - - - - - - - 站点内链爬取程序- - - - - - - - - - - - - -")
    print("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")

    for site_item in site_list:
        result_url_list = []
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                # re_string = r"(\.png)|(\.jpg)"
                # page.route(re.compile(re_string), cancel_request)
                site_url_str = "http://" + site_item
                result_url_list = gain_website_url(site_url_str)
                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)
            fail_log.append(["站点链接抓取失败,", e_site_fail])

        if len(result_url_list) == 0:
            try:
                with sync_playwright() as p:
                    # 启动浏览器
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    # re_string = r"(\.png)|(\.jpg)"
                    # page.route(re.compile(re_string), cancel_request)
                    site_url_str = "https://" + site_item
                    result_url_list = gain_website_url(site_url_str)
                    # 关闭浏览器
                    browser.close()
            except Exception as e_site_fail:
                print("站点链接抓取失败，", e_site_fail)
                fail_log.append(["站点链接抓取失败，", e_site_fail])

        # print(result_url_list)

        site_item_str = site_item.replace(".", "")
        save_path = "./" + site_item_str + ".csv"
        write_to_csv(result_url_list, save_path, ["stage2link", "stage3link"])

    print("Fail Log:", fail_log)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")


"""
bug1) 当前访问二级链： mailto:president@swu.edu.cn, 需对邮箱的连接做处理

bug2) 相对目录案例
https://www.cqxyfl.com/index.htm
href="index!loadMenu.action?preid=560001&id=2c9a808672e400070172e40320780004"

http://jdgc.cqgmy.cn/
href="info/1004/2217.htm"

内链样式提取:

href="http://www.cqcivc.edu.cn/xwzx2020/15512.html"
href="info/1004/2217.htm"
href="index!loadMenu.action?preid=560001&id=2c9a808672e400070172e40320780004"

"./XXXX"、"XXXX/XXXX/"、"XXXX"
"/XXXXX"
"//"

"""

"""

爬取实验1(playwright优化前)：www.mryu.top, 754秒，67个二级链接，2904个三级链接
爬取实验2(playwright全面放开限速等待):www.mryu.top, 91秒，67个二级链接，2904个三级链接
爬取实验3(做了去重，且限制图片加载):www.mryu.top, 347秒，66个二级链接，1899个三级链接
爬虫实验4(采用page.wait_for_load_state("networkidle")，即500ms内没有网络连接，秒啊):www.mryu.top,130秒，66个二级链接，1899个三级链接

记录：
www.cqmg.gov.cn，此网站超级慢,用传统的time.sleep()，是可以的，但会影响其他网站的整体爬取

"""
