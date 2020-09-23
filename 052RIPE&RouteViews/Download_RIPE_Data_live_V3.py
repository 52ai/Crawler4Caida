# coding:utf-8
"""
create on Sep 16, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

实时获取RIPE 所有节点Update数据。（RIPE每隔5分钟生成一个Update报文包，并将其放在FTP中，延时为5分钟）
因此，我只需要每隔五分钟去获取一次实时的BGP Update数据

V2:
直接获取年月数据，使用连接http://data.ris.ripe.net/rrc00/2020.09/
拿到更提前5分钟的数据，其latest-update.gz，要把文件夹中的数据晚5分钟
此外，加入递归下载以处理网络不稳定的情况

V3:
处理了requests请求错误异常

"""

import wget
import time
import os
import threading
import datetime
from bs4 import BeautifulSoup
import requests


def gain_latest_update_url(page_url):
    """
    根据月份文件夹，获取当前月份最新的update报文数据
    :param page_url:
    :return latest_update_url:
    """
    page_html = requests.get(page_url)
    bs_obj = BeautifulSoup(page_html.text, "html5lib")
    time.sleep(10)
    tr_list = bs_obj.find("tbody").findAll("tr")
    for tr_item in tr_list:
        a_item = tr_item.find("a")
        if a_item:
            url_str = a_item.attrs['href']
            if url_str.find("gz") != -1:
                latest_update_url = page_url + url_str
                return latest_update_url


def download_file(file_url):
    """
    根据传入的url,按照节点下载最新的BGP Update报文，分文件夹存储
    :param file_url:
    :return:
    """
    # print(file_url)
    file_url_split = file_url.split("/")
    # print(file_url_split)
    rrc_flag = file_url_split[3]
    file_flag = file_url_split[5]
    dir_path = "../000LocalData/BGPData/ripe/live_data/" + rrc_flag + "/"
    file_path = dir_path + file_flag
    print(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    wget.download(file_url, file_path)


def download_file_live(rrc):
    """
    定时监控rrc的目录，每隔5分钟下载一个最新BGP Update报文
    :param rrc:
    :return:
    """
    while True:
        try:
            datetime_local = datetime.datetime.fromtimestamp(time.time())
            datetime_utc = (datetime_local - datetime.timedelta(hours=8))
            time_str = datetime_utc.strftime("%Y.%m")  # 获取当前的年、月字符串
            rrc_latest_month_url = "http://data.ris.ripe.net/" + rrc + "/" + time_str + "/"  # 拼接月份文件夹
            rrc_latest_update_url = gain_latest_update_url(rrc_latest_month_url)  # 获取最新连接
            download_file(rrc_latest_update_url)
        except Exception as e:
            print("Download Error:", e)
        time.sleep(5*60)  # 休眠5分钟


if __name__ == "__main__":
    time_start = time.time()
    # RIPE历史数据 rrc17无效，其余均有效
    # RIPE实时数据 rrc02、rrc08、rrc09无效，其余均有效
    # rrc_list = ["rrc00", "rrc01", "rrc03", "rrc04",
    #             "rrc05", "rrc06", "rrc07",
    #             "rrc10", "rrc11", "rrc12", "rrc13", "rrc14",
    #             "rrc15", "rrc16", "rrc18", "rrc19",
    #             "rrc20", "rrc21", "rrc22", "rrc23", "rrc24"]
    rrc_list = ["rrc00"]
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
