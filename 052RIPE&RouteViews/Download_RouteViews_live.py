# coding:utf-8
"""
create on Sep 17, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:
参考已实现的RIPE实时数据采集程序，完成RouteViews 30个节点的实时采集程序
"""

import wget
import time
import os
import threading
import datetime
from bs4 import BeautifulSoup
import requests

rrc_dict = {"rrc00": "http://archive.routeviews.org/bgpdata",
            "rrc01": "http://archive.routeviews.org/route-views3/bgpdata",
            "rrc02": "http://archive.routeviews.org/route-views4/bgpdata",
            "rrc03": "http://archive.routeviews.org/route-views6/bgpdata",
            "rrc04": "http://archive.routeviews.org/route-views.amsix/bgpdata",
            "rrc05": "http://archive.routeviews.org/route-views.chicago/bgpdata",
            "rrc06": "http://archive.routeviews.org/route-views.chile/bgpdata",
            "rrc07": "http://archive.routeviews.org/route-views.eqix/bgpdata",
            "rrc08": "http://archive.routeviews.org/route-views.flix/bgpdata",
            "rrc09": "http://archive.routeviews.org/route-views.gorex/bgpdata",
            "rrc10": "http://archive.routeviews.org/route-views.isc/bgpdata",
            "rrc11": "http://archive.routeviews.org/route-views.kixp/bgpdata",
            "rrc12": "http://archive.routeviews.org/route-views.jinx/bgpdata",
            "rrc13": "http://archive.routeviews.org/route-views.linx/bgpdata",
            "rrc14": "http://archive.routeviews.org/route-views.napafrica/bgpdata",
            "rrc15": "http://archive.routeviews.org/route-views.nwax/bgpdata",
            "rrc16": "http://archive.routeviews.org/route-views.phoix/bgpdata",
            "rrc17": "http://archive.routeviews.org/route-views.telxatl/bgpdata",
            "rrc18": "http://archive.routeviews.org/route-views.wide/bgpdata",
            "rrc19": "http://archive.routeviews.org/route-views.sydney/bgpdata",
            "rrc20": "http://archive.routeviews.org/route-views.saopaulo/bgpdata",
            "rrc21": "http://archive.routeviews.org/route-views2.saopaulo/bgpdata",
            "rrc22": "http://archive.routeviews.org/route-views.sg/bgpdata",
            "rrc23": "http://archive.routeviews.org/route-views.perth/bgpdata",
            "rrc24": "http://archive.routeviews.org/route-views.sfmix/bgpdata",
            "rrc25": "http://archive.routeviews.org/route-views.soxrs/bgpdata",
            "rrc26": "http://archive.routeviews.org/route-views.mwix/bgpdata",
            "rrc27": "http://archive.routeviews.org/route-views.rio/bgpdata",
            "rrc28": "http://archive.routeviews.org/route-views.fortaleza/bgpdata",
            "rrc29": "http://archive.routeviews.org/route-views.gixa/bgpdata"}


def gain_latest_update_url(page_url):
    """
    根据月份文件夹，获取当前月份的最新update报文
    :param page_url:
    :return latest_update_url:
    """
    print(page_url)
    page_html = requests.get(page_url)
    bs_obj = BeautifulSoup(page_html.text, "html5lib")
    time.sleep(1)
    tr_list = bs_obj.find("tbody").findAll("tr")
    for tr_item in tr_list:
        a_item = tr_item.find("a")
        if a_item:
            url_str = a_item.attrs['href']
            if url_str.find("bz2") != -1:
                latest_update_url = page_url.strip("?C=M;O=D") + url_str
                return latest_update_url


def download_file(file_url, rrc):
    """
    根据传入的url，按照节点下载最新的BGP Update报文，分文件夹存储
    :param file_url:
    :param rrc:
    :return:
    """
    print(file_url)
    file_url_split = file_url.split("/")
    print(file_url_split)
    file_flag = file_url_split[-1]
    dir_path = "../000LocalData/BGPData/route-views/live_data/" + rrc + "/"
    file_path = dir_path + file_flag
    print(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    wget.download(file_url, file_path)


def download_file_live(rrc):
    """
    定时监控rrc的目录，每个15分钟下载一个最新的BGP Update报文
    :param rrc:
    :return:
    """
    while True:
        try:
            datetime_local = datetime.datetime.fromtimestamp(time.time())
            datetime_utc = (datetime_local - datetime.timedelta(hours=8))
            time_str = datetime_utc.strftime("%Y.%m")  # 获取当前的年、月字符串
            rrc_latest_month_url = rrc_dict[rrc] + "/" + time_str + "/UPDATES/?C=M;O=D"  # 拼接月份文件夹
            rrc_latest_update_url = gain_latest_update_url(rrc_latest_month_url)  # 获取最新链接
            download_file(rrc_latest_update_url, rrc)
        except Exception as e:
            print("Download Error:", e)
        time.sleep(15*60)  # 休眠15分钟


if __name__ == "__main__":
    time_start = time.time()
    # RouteViews实时数据 rrc12、rrc29无效，其余均有效
    rrc_list = ["rrc00", "rrc01", "rrc02", "rrc03", "rrc04",
                "rrc05", "rrc06", "rrc07", "rrc08", "rrc09",
                "rrc10", "rrc11", "rrc13", "rrc14",
                "rrc15", "rrc16", "rrc17", "rrc18", "rrc19",
                "rrc20", "rrc21", "rrc22", "rrc23", "rrc24",
                "rrc25", "rrc26", "rrc27", "rrc28"]
    """
    采用多线程，监控25个节点，每隔5分钟爬取一次最新的Update报文
    """
    threads = []  # 存储线程
    for rrc_item in rrc_list:
        threads.append(threading.Thread(target=download_file_live, args=(rrc_item,)))
    for t in threads:
        t.setDaemon(True)
        t.start()
    # 必须等待for循环里面所有线程都结束后，再执行主线程
    for k in threads:
        k.join()
    print("All threading finished!")

    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")