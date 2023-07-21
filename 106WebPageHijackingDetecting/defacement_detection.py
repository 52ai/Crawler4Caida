# coding:utf-8
"""
create on Jul. 20 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

前期已完成国内域名列表获取，初始化快照库构建工作。
此程序先通过预置一些简单的规则，如文件大小、关键词检索（如hacked by）等方式，形成一个篡改检测Demo

主要思路：
1）遍历待检测域名列表；
2）针对每一个域名开展检测，计算文本相似度（TFIDF）以及关键词特征；
3）根据上述特征判断该页面是否存在篡改。

"""
import re
import time
import os
from urllib.parse import urlparse
import threading
from selenium import webdriver
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from shutil import copyfile


def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return html_content


def clean_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()

    cleaned_text = re.sub(r'\s+', '', text).strip()
    return cleaned_text


def calculate_similarity(doc1, doc2):
    # 将文本数据转换为TF-IDF向量
    vec = TfidfVectorizer()
    tfidf_matrix = vec.fit_transform([doc1, doc2])
    # 计算余弦相似度
    similarity_matrix = cosine_similarity(tfidf_matrix)
    # 取出相似度矩阵中的相似度值
    similarity = similarity_matrix[0, 1]
    return similarity


def run_page_list_info_detection_selenium(run_page_list):
    """
    根据传入的page list，多线程爬取页面信息
    :param run_page_list:
    :return:
    """
    # 启动浏览器
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.set_page_load_timeout(15)
    driver.implicitly_wait(10)  # 设置隐性等待时间
    # driver.set_window_size(width=1280, height=720)
    # 遍历传入的page url list
    for run_page in run_page_list:
        time_format_date = "%Y%m%d"
        time_date_str = time.strftime(time_format_date, time.localtime())
        data_dir = "../000LocalData/106WebPage/" + time_date_str
        data_dir_origin = "../000LocalData/106WebPage/20230715_origin"

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print("Create Directory:", data_dir)

        domain_name = urlparse(run_page).netloc
        site_str = domain_name.replace(".", "_")
        save_path_png = data_dir + "/" + site_str + ".png"
        save_path_html = data_dir + "/" + site_str + ".html"

        origin_path_png = data_dir_origin + "/" + site_str + ".png"
        origin_path_html = data_dir_origin + "/" + site_str + ".html"

        origin_path_png_dst = data_dir + "/" + site_str + "_origin.png"
        origin_path_html_dst = data_dir + "/" + site_str + "_origin.html"

        if not os.path.exists(origin_path_png) or not os.path.exists(origin_path_html):
            # print("No Crawler, Next!")
            continue

        try:
            driver.get(run_page)
            page_html = driver.page_source
            # 获取网站截图，并保存到本地
            driver.save_screenshot(save_path_png)
            with open(save_path_html, "w", encoding="utf-8") as f_html:
                f_html.write(page_html)
            """"
            以下为检测程序
            """
            doc1 = read_html_file(save_path_html)
            doc2 = read_html_file(origin_path_html)

            doc1_cleaned = clean_html(doc1)
            doc2_cleaned = clean_html(doc2)

            # print(doc1_cleaned)
            # 计算历史信息库的TF-IDF文档相似度
            similarity_percentage = calculate_similarity(doc1_cleaned, doc2_cleaned)

            hacked_flag = "否"
            if doc1_cleaned.find("hackedby") != -1:
                hacked_flag = "是"

            if similarity_percentage < 0.1 or hacked_flag == "是":
                print("-------------------------------")
                print("url:", run_page)
                print("获取当前页面状态成功!")
                print("历史匹配TF-IDF文档相似度：", similarity_percentage)
                print("是否含被篡改关键字：", hacked_flag)
                # 相似度小于0.1，则输出网站截图及原始截图
                copyfile(origin_path_png, origin_path_png_dst)
                copyfile(origin_path_html, origin_path_html_dst)
                print("检测结论：该页面疑似篡改!!!")
            else:
                # print("检测结论：该页面未被篡改")
                # 若未被篡改，则删除记录
                os.remove(save_path_png)
                os.remove(save_path_html)

        except Exception as e:
            # print(f"Failed! Info({run_page}):")
            # print(e)
            if str(e).find("without establishing a connection") != -1:
                print("without establishing a connection：连接关闭！！！刷新下浏览器")
                driver.refresh()  # 刷新的浏览器

    # 关闭浏览器
    driver.quit()


def run_main():
    """
    主程序
    :return:
    """
    time_format = "%Y%m%d %H:%M:%S"
    time_str = time.strftime(time_format, time.localtime())
    print("===启动国内域名篡改检测程序：", time_str)

    """
    第一步，获取待检测的列表，并按照并发线程数将其拆分为不同分任务列表
    """
    page_list_all = []  # 原始page url 列表
    page_list_group = []  # 分组page url
    n_threading = 1  # 设置并发线程数

    cn_domains_file = "../000LocalData/106WebPage/cn_domains_test.csv"
    with open(cn_domains_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            page_url = "http://" + line[0]
            page_list_all.append(page_url)

    max_page_cnt = (len(page_list_all) // n_threading) + 1  # 向上取整
    print("page list all:", len(page_list_all))
    print("threading:", n_threading)
    print("max_page_cnt:", max_page_cnt)

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
    """
    第二步：将分组后的任务列表，分给不同的线程独立执行
    """
    threads = []  # 存储线程
    for group_list in page_list_group:
        threads.append(threading.Thread(target=run_page_list_info_detection_selenium, args=(group_list,)))
    for t in threads:
        t.setDaemon(True)
        t.start()

    # 必须等待for循环里面所有的线程都结束，再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")


if __name__ == '__main__':
    time_start = time.time()
    loop = 1
    max_loop = loop + 1
    while loop:
        print(f"第{max_loop-loop}次循环")
        run_main()
        loop -= 1
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
