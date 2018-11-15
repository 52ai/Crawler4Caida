# coding:utf-8
"""
Create on Nov 13, 2018 by Wayne Yu
Function: Get music 163 artists info
主要是温习两件事：第一、静态页面的爬取分析；第二、动态页面的爬取分析。
注：动态页面的爬取如果能够找到JS加载的方法，就直接采用JS破解，使用本地浏览器测试运行的方法速度一般比较慢。
=>此次动态页面的爬取采用Python+Selenium+Firefox的组合。（此前使用的是Python+Selenium+PhantomJs的组合）
Python(3.7) + Selenium(3.141.0) + Firefox(63.0.1)
=>静态页面的分析使用BeautifulSoup(4.6.3)
需要下载firefox驱动并放在目录中。（驱动下载地址：https://github.com/mozilla/geckodriver/releases）
windows:Python的安装目录scripts中，Mac放置在/user/local/bin中

1) selenium的版本要足够高，以适配最新版的firefox浏览器。（起初一直运行失败的原因在于selenium的版本不够高）
2) 获取加载之后的页面信息，使用的是run_firefox.page_info方法。（至于其他的用法需要摸索，比如运行JS、定位元素等方法）
3）关于Selenium WebDriver的使用方法，可以参考链接：https://www.seleniumhq.org/docs/03_webdriver.jsp
4）关于BeautifulSoup的使用方法，可以参考链接：https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html
5）但是到了动态加载之后，爬虫精进并没有结束，还有加密、模拟登陆、验证码等问题需要研究。
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def get_artists_info(url):
    """
    抓取网易云音乐歌手页面的动态信息，并根据要求返回相关信息
    :param url:
    :return:artists_info
    """
    # html = urlopen(url)
    run_firefox = webdriver.Firefox()
    run_firefox.get(url)
    # 获取cookie信息
    # cookies = run_firefox.get_cookies()
    # print(cookies)
    print(run_firefox.title)
    # ele = run_firefox.find_element(By.NAME, "name")  # find the search box
    # print(ele)
    # ele.clear()
    # ele.send_keys("18106")
    # ele.submit()
    time.sleep(3)
    run_firefox.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    # print(run_firefox.page_source)
    time.sleep(3)
    # run_firefox.execute_script('alert("ToBottom")')
    run_firefox.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(3)
    bs_obj = BeautifulSoup(run_firefox.page_source, "html5lib")
    print(bs_obj)
    run_firefox.quit()
    return "OK!"


if __name__ == "__main__":
    # page_url = "https://music.163.com/#/artist?id=8103"
    # page_url = "https://xueqiu.com/#/cn"
    # page_url = "https://music.163.com/#/artist/desc?id=8103"  # 花粥的简介及个人资料
    # page_url = "https://music.163.com/artist/desc?id=8103"
    # page_url = "http://as-rank.caida.org/asns/3549?page=1&count=40&page=2"
    page_url = "https://wenku.baidu.com/view/0ccb2226a5e9856a561260f0.html"
    print(get_artists_info(page_url))
    # print(urlopen(page_url))

