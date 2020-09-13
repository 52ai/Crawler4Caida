# coding:utf-8
""""
create on Sep 7, 2020 By Wenyan YU

Function:
根据RIPE历史文件url,按照节点和月份，分别存储数据

"""
import wget
import time
import os
import urllib.request

download_links_ripe = "all_download_links_ripe.csv"


def download_file(file_url):
    """
    根据传入url，按照节点和月份，分文件夹存储数据
    :param file_url:
    :return:
    """
    print(file_url)
    file_url_split = file_url.split("/")
    print(file_url_split)
    rrc_flag = file_url_split[3]
    time_flag = file_url_split[4]
    file_flag = file_url_split[5]
    dir_path = "./ripe/" + rrc_flag + "/" + time_flag + "/"
    file_path = dir_path + file_flag
    print(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    wget.download(file_url, file_path)
    # urllib.request.urlretrieve(file_url, file_path)


if __name__ == "__main__":
    time_start = time.time()
    download_links_ripe_read = open(download_links_ripe, "r", encoding='utf-8')
    for url_item in download_links_ripe_read.readlines()[8426:]:
        try:
            download_file(url_item.strip())
        except Exception as e:
            print(e)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
