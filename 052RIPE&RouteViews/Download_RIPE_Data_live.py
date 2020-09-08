# coding:utf-8
"""
create on Sep 7, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

实时获取RIPE 所有节点Update数据。（RIPE每隔5分钟生成一个Update报文包，并将其放在FTP中，延时为5分钟）
因此，我只需要每隔五分钟去获取一次实时的BGP Update数据

"""

import wget
import time
import os
import threading
import datetime


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
    file_flag = file_url_split[4]
    dir_path = "./ripe/live_data/" + rrc_flag + "/"
    datetime_local = datetime.datetime.fromtimestamp(time.time())
    datetime_utc = (datetime_local - datetime.timedelta(hours=8))
    time_str = datetime_utc.strftime("%Y%m%d.%H%M")
    # print(time.time())
    file_path = dir_path + time_str + "-" + file_flag
    print(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:
        wget.download(file_url, file_path)
    except Exception as e:
        print(e)


def download_file_live(rrc):
    """
    定时监控rrc的目录，每隔5分钟下载一个最新BGP Update报文
    :param rrc:
    :return:
    """
    # print(rrc)
    rrc_latest_update_url = "http://data.ris.ripe.net/" + rrc + "/latest-update.gz"
    while True:
        download_file(rrc_latest_update_url)
        time.sleep(60*5)  # 休眠5分钟


if __name__ == "__main__":
    time_start = time.time()
    # RIPE rrc17无效，其余均有效
    rrc_list = ["rrc00", "rrc01", "rrc02", "rrc03", "rrc04",
                "rrc05", "rrc06", "rrc07", "rrc08", "rrc09",
                "rrc10", "rrc11", "rrc12", "rrc13", "rrc14",
                "rrc15", "rrc16", "rrc18", "rrc19",
                "rrc20", "rrc21", "rrc22", "rrc23", "rrc24"]
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
