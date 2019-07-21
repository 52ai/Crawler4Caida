# coding:utf-8
"""
Create on July 21,2019 by Wayne
程序功能：
V1:获取给定网站的截图和html源文件
V2:新增部署相关功能（Python3.7 + Selenium3.141.0 + firefox 68.0.1），部署说明见README.md

基本思路：
读取给定网站列表，通过Python访问每个网站，截图并保存html源文件

"""

from selenium import webdriver
import time

mylog = []

def get_page_info(page_url, page_cnt):
    """
    :param page_url, page_cnt:
    :return: None
    """
    # 对page_url进行统一处理，判断是否有https、http、www，若没有则进行相应的格式调整
    if "www." not in page_url:
        page_url = "www." + page_url
    if "http" not in page_url:
        page_url = "http://"+page_url
    print(page_cnt, ":", page_url)
    log_str = page_cnt, ":", page_url, "\n"
    mylog.append(log_str)

    # 访问统一格式之后的网址
    driver.get(page_url)
    # 获取网页的html信息
    # print(driver.page_source)
    page_html = driver.page_source
    # 获取网站截图，并保存到本地
    driver.save_screenshot("./website_"+str(page_cnt)+"_screen.png")
    # print(page_html)
    write_file_name = "./website_"+str(page_cnt)+"_source.html"
    with open(write_file_name, "w", encoding="utf-8") as f:
        f.write(page_html)


if __name__ == "__main__":
    # web_url = "http://www.365guanainin.com"
    time_start = time.time()  # 记录启动的时间
    # 启动浏览器
    driver = webdriver.Firefox()
    driver.maximize_window()
    # 读取网站列表
    webList_file = "./content.csv"
    webList = open(webList_file, "r", encoding="utf-8")
    line_cnt = 0
    for line in webList.readlines():
        if line_cnt == 0:
            line_cnt += 1
            continue
        line_cnt += 1  # 行计数自增1
        # print(line.split(",")[1])
        web_url = line.split(",")[1]
        # 对网站进行统一处理，先去掉http、www前缀，然后再统一访问格式
        # web_url = urlparse(web_url)
        # print(web_url)
        # 网站存在打不开的情况，需要对打不开的网站做相应的异常处理
        try:
            get_page_info(web_url, line_cnt)
        except Exception as e:
            print(line_cnt, ":Error!Continue…")
            log_str = line_cnt, ":Error!Continue…"
            mylog.append(log_str)
            continue
    # 关闭浏览器
    driver.quit()
    time_end = time.time()  # 记录结束的时间
    print("=>SCRIPTS FINISH, TIME CONSUMING:", (time_end - time_start), "s")
    log_str = "=>SCRIPTS FINISH, TIME CONSUMING:", (time_end - time_start), "s"
    mylog.append(log_str)
    # 输出程序运行日志
    log_file_name = "./exe_log.log"
    with open(log_file_name, "w", encoding="utf-8") as f:
        mylog = str(mylog)
        f.write(mylog)