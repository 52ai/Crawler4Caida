# coding:utf-8
""""
create on July 2, 2021 By Wenyan YU
Function:

6月30日，李博士提到：
“能否抽一下全球ix，看看星云图、极图情况？”
“要么就是把互联点表达出来，点用颜色表示，就是把与ix无关的线去掉”

我理解就是要对”全球IX可视化开展研究“
在此之前，需要把全球IX的详细信息，初步考虑先从PEERING DB中取全球IX的全集，然后再结合Google Map，提取经纬度


经研究，
PEERING DB的IX信息中存在许多异常时，比如填写不规范等，若人工处理太费劲，好在HE的数据还能凑活用，数据为ix_he.CSV

"""

from urllib.request import urlopen
import json
from datetime import *
import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    # print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def ix_crawler():
    """
    基于PEERING DB数据抽取全球IX数据
    :return:
    """
    html = urlopen(r"https://www.peeringdb.com/api/ix")
    html_json = json.loads(html.read())
    ix_list = []  # 存储全部的ix信息
    for item in html_json['data']:
        # print(item)
        ix_id = item["id"]
        ix_name = item["name"]
        # ix_name_long = item["name_long"]
        ix_city = item["city"]
        ix_country = item["country"]
        ix_net_count = item["net_count"]
        ix_created = item["created"]
        ix_updated = item["updated"]
        # temp_list = [ix_id, ix_name, ix_name_long, ix_city, ix_country, ix_net_count, ix_created, ix_updated]
        temp_list = [ix_id, ix_name, ix_city, ix_country, ix_net_count, ix_created, ix_updated]
        # print(temp_list)
        ix_list.append(temp_list)
    print("统计时间:", datetime.now())
    print("当前全球IX数量为:", len(ix_list))
    save_path = "./ix.csv"
    write_to_csv(ix_list, save_path)


if __name__ == "__main__":
    time_start = time.time()
    ix_crawler()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end-time_start), "S")
