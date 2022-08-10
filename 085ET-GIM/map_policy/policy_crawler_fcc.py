# coding:utf-8
"""
create on Aug 10, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

该程序实现对US  FCC网站政策环境的抓取功能（2002年至今）

入口url: https://www.fcc.gov/news-events/headlines
单条记录url示例: https://www.fcc.gov/document/fcc-launches-proceeding-revoking-china-telecoms-authorizations-0
每条政策动态记录包括：
released_date, title, full_title, document_type, bureau, description,attachment_url, url

"""

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s>.." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        for i in res_list:
            writer.writerow(i)
    except Exception as e_csv:
        print(e_csv)
    finally:
        csv_file.close()
    print("write finish!")


def gain_news_detail(page_url):
    """
    根据政策动态url，获悉详细信息
    title, full_title, document_type, bureau, description, attachment_url
    :param page_url:
    :return news_detail:
    """
    news_page.goto(page_url)
    news_page.wait_for_load_state("load")
    news_page_html = news_page.content()
    bs_obj = BeautifulSoup(news_page_html, "html5lib")

    full_title = "unknown"
    document_type = "unknown"
    bureau = "unknown"
    description = "unknown"
    attachment_url = "unknown"

    # print(bs_obj)
    title = bs_obj.find("h1", {"id": "page-title"}).get_text()

    try:
        docs = bs_obj.find("ul", {"class": "edocs"})
        if docs:
            li_list = docs.findAll("li")
            full_title = li_list[0].get_text().strip("Full Title:").strip()
            document_type = li_list[1].get_text().strip("Document Type(s):").strip()
            bureau = li_list[2].get_text().strip("Bureau(s):").strip()

        descr = bs_obj.find("div", {"class": "section--left-80"})
        if descr:
            p_list = descr.findAll("p")
            if len(p_list) == 3:
                description = p_list[2].get_text().strip("Description:").strip()

        attachment_pdf = bs_obj.find("a", {"class": "attachment pdf"})
        if attachment_pdf:
            attachment_url = attachment_pdf.attrs["href"]
    except Exception as e:
        print(e)

    news_detail = [title, full_title, document_type, bureau, description, attachment_url]

    return news_detail


def gain_news_info(site_url):
    """
    根据入口地址，获取政策动态列表
    结合gain_news_detail，最终获取全集信息
    released_date, title, full_title, document_type, bureau, description, file_link, url
    :param site_url:
    :return result_list:
    """
    result_list = []  # 存储最终的结果
    page.goto(site_url)
    page.wait_for_load_state("networkidle")
    page_html = page.content()
    bs_obj = BeautifulSoup(page_html, "html5lib")
    while True:
        temp_line = []  # 临时存储单条记录
        for item in bs_obj.findAll("article"):
            page_url = "https://www.fcc.gov" + item.attrs['about']
            release_date = item.find("span", {"class": "released-date"}).get_text().split("-")[0]
            release_date = release_date.strip()
            print(page_url, release_date)
            news_detail = gain_news_detail(page_url)
            # print(news_detail)
            temp_line.append(release_date)
            temp_line.extend(news_detail)
            temp_line.append(page_url)
            with open("./fcc_policy.csv", "a", newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerow(temp_line)
            temp_line = []

        page_next = bs_obj.find("a", {"title": "Go to next page"})
        if page_next:
            # if Go to next page is not none, go to next page
            page_next_url = "https://www.fcc.gov" + page_next.attrs['href']
            print(page_next_url)
            page.goto(page_next_url)
            page_html = page.content()
            bs_obj = BeautifulSoup(page_html, "html5lib")
        else:
            # if Go to
            break

    return result_list


if __name__ == "__main__":
    fcc_url = "https://www.fcc.gov/news-events/headlines?page=20"
    time_start = time.time()  # 记录程序的启动时间
    print("- - - - - - - - - - - - 爬取程序- - - - - - - - - - - - - -")
    print("程序启动时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "\n")
    try:
        with sync_playwright() as p:
            # 启动浏览器
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            news_page = browser.new_page()
            result = gain_news_info(fcc_url)
            # 关闭浏览器
            browser.close()
    except Exception as e_site_fail:
        print("站点链接抓取失败，", e_site_fail)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
