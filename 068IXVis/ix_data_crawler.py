# coding:utf-8
""""
create on July 2, 2021 By Wenyan YU
Function:

6月30日，李博士提到：
“能否抽一下全球ix，看看星云图、极图情况？”
“要么就是把互联点表达出来，点用颜色表示，就是把与ix无关的线去掉”

我理解就是要对”全球IX可视化开展研究“
在此之前，需要把全球IX的详细信息，初步考虑先从PEERING DB中取全球IX的全集，然后再结合Google Map，提取经纬度

"""

from urllib.request import urlopen
import json
from datetime import *
import time


def ix_crawler():
    """
    基于PEERING DB数据抽取全球IX数据
    :return:
    """
    html = urlopen(r"https://www.peeringdb.com/api/ix")
    html_json = json.loads(html.read())
    for item in html_json['data']:
        print(item)
        ix_name = item["name"]


if __name__ == "__main__":
    time_start = time.time()
    ix_crawler()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")