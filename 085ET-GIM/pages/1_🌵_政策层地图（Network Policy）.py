import streamlit as st
import time
import numpy as np
import re
import pandas as pd
from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse
import os


import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud
import urllib.request
import html2text
from PIL import Image

st.set_page_config(
    page_title="政策层地图",
    page_icon="world_map",
    layout="centered",
)

# 去除streamlit的原生标记
sys_menu = '''
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
'''
st.markdown(sys_menu, unsafe_allow_html=True)

if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.user = "Guest"

# 给侧边栏添加APP版本信息
with st.sidebar:
    st.write("Login:", st.session_state.user)
    st.sidebar.markdown(
        """
        <small> ET-GIM 0.1.0 | Jane 2022 </small>  
        <small> Driven By PYTHON </small>
         """,
        unsafe_allow_html=True,
    )


if st.session_state.count > 0:
    menu = ["全球", "中国", "美国", "俄罗斯", "德国", "日本"]
    choice = st.sidebar.selectbox("请选择目标国家或地区：", menu)
    headless_radio = st.sidebar.radio("请选择是否使用headless参数爬取页面：", (True, False))

    if choice == "全球":
        st.write("全球各国网络政策环境源首页动态-实时抓取")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        st.write("页面实时抓取中...")
        time_format = "%Y%m"   # 通过调整time_format，可实现按月或按天加载截图

        with sync_playwright() as p:
            # 启动浏览器
            page_url = "https://www.miit.gov.cn/"
            st.write("源站：中华人民共和国工业和信息化部（MIIT）")
            st.write("URL:", page_url)
            domain_name = urlparse(page_url).netloc.strip("www.")
            site_str = domain_name.replace(".", "")
            save_path = "./cache/" + site_str + time.strftime(time_format, time.localtime()) + ".png"
            if not os.access(save_path, os.F_OK):
                # 判断今天是否已经截图了
                browser = p.firefox.launch(headless=headless_radio)
                page = browser.new_page()  # 如果没有截图，再打开新界面
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=save_path)
            st.image(save_path)

            st.markdown("---")

            page_url = "https://www.fcc.gov/news-events"
            st.write("源站：美国联邦通信委员会（FCC）")
            st.write("URL:", page_url)
            domain_name = urlparse(page_url).netloc.strip("www.")
            site_str = domain_name.replace(".", "")
            save_path = "./cache/" + site_str + time.strftime(time_format, time.localtime()) + ".png"
            if not os.access(save_path, os.F_OK):
                # 判断今天是否已经截图了
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=save_path)
            st.image(save_path)

            st.markdown("---")

            page_url = "https://rkn.gov.ru/"
            st.write("源站：俄罗斯联邦通信、信息技术和大众传媒监督局（RKN）")
            st.write("URL:", page_url)
            domain_name = urlparse(page_url).netloc.strip("www.")
            site_str = domain_name.replace(".", "")
            save_path = "./cache/" + site_str + time.strftime(time_format, time.localtime()) + ".png"
            if not os.access(save_path, os.F_OK):
                # 判断今天是否已经截图了
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=save_path)
            st.image(save_path)

            st.markdown("---")

            page_url = "https://www.bundesnetzagentur.de"
            st.write("源站：德国联邦网络管理局(Federal Network Agency) (BNetzA)")
            st.write("URL:", page_url)
            domain_name = urlparse(page_url).netloc.strip("www.")
            site_str = domain_name.replace(".", "")
            save_path = "./cache/" + site_str + time.strftime(time_format, time.localtime()) + ".png"
            if not os.access(save_path, os.F_OK):
                # 判断今天是否已经截图了
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=save_path)
            st.image(save_path)

            st.markdown("---")

            page_url = "https://www.soumu.go.jp"
            st.write("源站：日本公共管理暨内务、邮政与电信通讯部（MPHPT）")
            st.write("URL:", page_url)
            domain_name = urlparse(page_url).netloc.strip("www.")
            site_str = domain_name.replace(".", "")
            save_path = "./cache/" + site_str + time.strftime(time_format, time.localtime()) + ".png"
            if not os.access(save_path, os.F_OK):
                # 判断今天是否已经截图了
                page.goto(page_url)
                page.wait_for_load_state("networkidle")
                page.screenshot(path=save_path)
            st.image(save_path)

            if 'browser' in globals():
                # 关闭浏览器, 先判断browser是否存在，再去关闭它
                browser.close()

    elif choice == "中国":
        page_url = "https://www.miit.gov.cn/"
        test_website = st.text_input("测试站点", value=page_url)
        st.write("您输入的测试的站点为", test_website)
        st.text("- - - - - - - - -政策层地图自动化分析程序- - - - - - - - --")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.webkit.launch(headless=headless_radio)
                page = browser.new_page()
                page.goto(test_website)
                page.wait_for_load_state("networkidle")

                with st.expander("网络政策环境页面实时抓取", True):
                    page.screenshot(path="./cache/screenshot.png")
                    st.image("./cache/screenshot.png")

                page_html = page.content()
                with st.expander("网络政策环境页面源码呈现", False):
                    st.code(page_html)

                with st.expander("提取网页源码关键文本内容", False):
                    h = html2text.HTML2Text()
                    h.ignore_links = True  # 去掉超链接
                    h.ignore_images = True
                    h.ignore_tables = True
                    text = h.handle(page_html)
                    st.write(text)

                with st.expander("基于自然语言处理文本分词", False):
                    text = text.replace(' ', '')
                    text = text.replace('*', '')
                    text = text.replace('\n', ' ')
                    cut_text = jieba.cut(text)  # 分词
                    result = " ".join(cut_text)
                    st.code(result)

                with st.expander("网络政策环境词云图可视化", True):
                    stop_words = set(open('./cache/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
                    wc = WordCloud(
                        font_path='./cache/仿宋_GB2312.ttf',
                        background_color='white',
                        width=1000,
                        height=600,
                        max_font_size=100,
                        min_font_size=5,
                        max_words=200,
                        # mask=plt.imread('star.jpg')  # mask图片
                        mode='RGBA',
                        stopwords=stop_words,
                        contour_width=1,
                    )
                    wc.generate(result)
                    save_path = './cache/wordcloud.png'
                    wc.to_file(save_path)  # 图片保存
                    st.image(save_path)

                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)

    elif choice == "美国":
        page_url = "https://www.fcc.gov/news-events"
        test_website = st.text_input("测试站点", value=page_url)
        st.write("您输入的测试的站点为", test_website)
        st.text("- - - - - - - - -政策层地图自动化分析程序- - - - - - - - --")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.firefox.launch(headless=headless_radio)
                page = browser.new_page()
                page.goto(test_website)
                page.wait_for_load_state("networkidle")

                with st.expander("网络政策环境页面实时抓取", True):
                    page.screenshot(path="./cache/screenshot.png")
                    st.image("./cache/screenshot.png")

                page_html = page.content()
                with st.expander("网络政策环境页面源码呈现", False):
                    st.code(page_html)

                with st.expander("提取网页源码关键文本内容", False):
                    h = html2text.HTML2Text()
                    h.ignore_links = True  # 去掉超链接
                    text = h.handle(page_html)
                    st.write(text)

                with st.expander("基于自然语言处理文本分词", False):
                    text = text.replace(' ', '')
                    text = text.replace('*', '')
                    text = text.replace('\n', ' ')
                    cut_text = jieba.cut(text)  # 分词
                    result = " ".join(cut_text)
                    st.code(result)

                with st.expander("网络政策环境词云图可视化", True):
                    stop_words = set(open('./cache/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
                    wc = WordCloud(
                        font_path='./cache/仿宋_GB2312.ttf',
                        background_color='white',
                        width=1000,
                        height=600,
                        max_font_size=100,
                        min_font_size=5,
                        max_words=200,
                        # mask=plt.imread('star.jpg')  # mask图片
                        mode='RGBA',
                        stopwords=stop_words,
                        contour_width=1,
                    )
                    wc.generate(result)
                    save_path = './cache/wordcloud.png'
                    wc.to_file(save_path)  # 图片保存
                    st.image(save_path)

                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)

    elif choice == "俄罗斯":
        page_url = "https://rkn.gov.ru/"
        test_website = st.text_input("测试站点", value=page_url)
        st.write("您输入的测试的站点为", test_website)
        st.text("- - - - - - - - -政策层地图自动化分析程序- - - - - - - - --")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.webkit.launch(headless=headless_radio)
                page = browser.new_page()
                page.goto(test_website)
                page.wait_for_load_state("networkidle")

                with st.expander("网络政策环境页面实时抓取", True):
                    page.screenshot(path="./cache/screenshot.png")
                    st.image("./cache/screenshot.png")

                page_html = page.content()
                with st.expander("网络政策环境页面源码呈现", False):
                    st.code(page_html)

                with st.expander("提取网页源码关键文本内容", False):
                    h = html2text.HTML2Text()
                    h.ignore_links = True  # 去掉超链接
                    text = h.handle(page_html)
                    st.write(text)

                with st.expander("基于自然语言处理文本分词", False):
                    text = text.replace(' ', '')
                    text = text.replace('*', '')
                    text = text.replace('\n', ' ')
                    cut_text = jieba.cut(text)  # 分词
                    result = " ".join(cut_text)
                    st.code(result)

                with st.expander("网络政策环境词云图可视化", True):
                    stop_words = set(open('./cache/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
                    wc = WordCloud(
                        font_path='./cache/仿宋_GB2312.ttf',
                        background_color='white',
                        width=1000,
                        height=600,
                        max_font_size=100,
                        min_font_size=5,
                        max_words=200,
                        # mask=plt.imread('star.jpg')  # mask图片
                        mode='RGBA',
                        stopwords=stop_words,
                        contour_width=1,
                    )
                    wc.generate(result)
                    save_path = './cache/wordcloud.png'
                    wc.to_file(save_path)  # 图片保存
                    st.image(save_path)
                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)

    elif choice == "德国":
        page_url = "https://www.bundesnetzagentur.de"
        test_website = st.text_input("测试站点", value=page_url)
        st.write("您输入的测试的站点为", test_website)
        st.text("- - - - - - - - -政策层地图自动化分析程序- - - - - - - - --")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.webkit.launch(headless=headless_radio)
                page = browser.new_page()
                page.goto(test_website)
                page.wait_for_load_state("networkidle")

                with st.expander("网络政策环境页面实时抓取", True):
                    page.screenshot(path="./cache/screenshot.png")
                    st.image("./cache/screenshot.png")

                page_html = page.content()
                with st.expander("网络政策环境页面源码呈现", False):
                    st.code(page_html)

                with st.expander("提取网页源码关键文本内容", False):
                    h = html2text.HTML2Text()
                    h.ignore_links = True  # 去掉超链接
                    text = h.handle(page_html)
                    st.write(text)

                with st.expander("基于自然语言处理文本分词", False):
                    text = text.replace(' ', '')
                    text = text.replace('*', '')
                    text = text.replace('\n', ' ')
                    cut_text = jieba.cut(text)  # 分词
                    result = " ".join(cut_text)
                    st.code(result)

                with st.expander("网络政策环境词云图可视化", True):
                    stop_words = set(open('./cache/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
                    wc = WordCloud(
                        font_path='./cache/仿宋_GB2312.ttf',
                        background_color='white',
                        width=1000,
                        height=600,
                        max_font_size=100,
                        min_font_size=5,
                        max_words=200,
                        # mask=plt.imread('star.jpg')  # mask图片
                        mode='RGBA',
                        stopwords=stop_words,
                        contour_width=1,
                    )
                    wc.generate(result)
                    save_path = './cache/wordcloud.png'
                    wc.to_file(save_path)  # 图片保存
                    st.image(save_path)
                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)

    elif choice == "日本":
        page_url = "https://www.soumu.go.jp"
        test_website = st.text_input("测试站点", value=page_url)
        st.write("您输入的测试的站点为", test_website)
        st.text("- - - - - - - - -政策层地图自动化分析程序- - - - - - - - --")
        st.write("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
        try:
            with sync_playwright() as p:
                # 启动浏览器
                browser = p.webkit.launch(headless=headless_radio)
                page = browser.new_page()
                page.goto(test_website)
                page.wait_for_load_state("networkidle")

                with st.expander("网络政策环境页面实时抓取", True):
                    page.screenshot(path="./cache/screenshot.png")
                    st.image("./cache/screenshot.png")

                page_html = page.content()
                with st.expander("网络政策环境页面源码呈现", False):
                    st.code(page_html)

                with st.expander("提取网页源码关键文本内容", False):
                    h = html2text.HTML2Text()
                    h.ignore_links = True  # 去掉超链接
                    text = h.handle(page_html)
                    st.write(text)

                with st.expander("基于自然语言处理文本分词", False):
                    text = text.replace(' ', '')
                    text = text.replace('*', '')
                    text = text.replace('\n', ' ')
                    cut_text = jieba.cut(text)  # 分词
                    result = " ".join(cut_text)
                    st.code(result)

                with st.expander("网络政策环境词云图可视化", True):
                    stop_words = set(open('./cache/cn_stopwords.txt', encoding="utf-8").read().split("\n"))
                    wc = WordCloud(
                        font_path='./cache/仿宋_GB2312.ttf',
                        background_color='white',
                        width=1000,
                        height=600,
                        max_font_size=100,
                        min_font_size=5,
                        max_words=200,
                        # mask=plt.imread('star.jpg')  # mask图片
                        mode='RGBA',
                        stopwords=stop_words,
                        contour_width=1,
                    )
                    wc.generate(result)
                    save_path = './cache/wordcloud.png'
                    wc.to_file(save_path)  # 图片保存
                    st.image(save_path)
                # 关闭浏览器
                browser.close()
        except Exception as e_site_fail:
            print("站点链接抓取失败，", e_site_fail)

else:
    st.info("请先点击首页下拉选择框，登录系统！")
