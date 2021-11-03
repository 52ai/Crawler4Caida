# coding: utf-8
"""
create on Nov 3, 2021 By Wenyan YU

Function:

因大屏数据更新需要，一雯姐那边对于全球IX数据有爬取需求
具体包括全球IX名称、接入网络数量、接入带宽、所属大洲（中英文）、所属国家（中英文）、所属城市（中英文）
其中接入带宽有两种方式可以获取，一是通过页面数据，直接抓取Total Speed；二是通过netixlan自己的分析整理出最终结果。
经研究可以通过方式二去做，再同方式一的结果进行核对，以保证数据分析结果的正确性

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
    :return None:
    """
    print("write file<%s> ..." % des_path)
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


def generate_ix_speed():
    """
    基于PEERDING DB数据抽取ix和net对应关系，并统计speed信息
    :return ix_speed_dict:
    """
    html = urlopen(r"https://www.peeringdb.com/api/netixlan")
    html_json = json.loads(html.read())
    ix_speed_dict = {}  # 存储ix的接入总带宽
    for item in html_json['data']:
        ix_id = item['ix_id']
        ix_speed = item['speed']
        if ix_id not in ix_speed_dict.keys():
            ix_speed_dict[ix_id] = ix_speed
        else:
            ix_speed_dict[ix_id] += ix_speed
    print("已成功统计 %s 个IX的speed信息" % len(ix_speed_dict))
    return ix_speed_dict


def generate_cn_translate():
    """
    根据国家缩写，转换国家（中文）和大洲（中文）信息
    :return cn_translate:
    """
    cn_translate = {}  # 存储转换后的中文信息
    file_in = "../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv"
    file_read = open(file_in, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        if line[4] not in cn_translate.keys():
            cn_translate[line[4]] = [line[5], line[3]]
        else:
            print(line)
            print("Repetitive Error!")
    print(cn_translate)
    return cn_translate


def ix_crawler():
    """
    基于PEERDING DB数据抽取全球IX数据
    :return None:
    """
    print("统计时间：", datetime.now())
    ix_speed = generate_ix_speed()
    cn_translate = generate_cn_translate()
    html = urlopen(r'https://www.peeringdb.com/api/ix')
    html_json = json.loads(html.read())
    ix_list = []  # 存储全部的ix信息
    for item in html_json['data']:
        ix_id = item["id"]
        ix_name = item["name"]
        ix_city = item["city"]
        ix_country = item["country"]
        ix_region = item['region_continent']
        ix_net_count = item["net_count"]
        try:
            ix_total_speed = ix_speed[ix_id]
        except Exception as e:
            print(e)
            ix_total_speed = 0
        temp_list = [ix_id, ix_name, ix_city, ix_country, ix_region, ix_net_count, ix_total_speed]
        cn_info = cn_translate[ix_country]
        temp_list.extend(cn_info)
        print(temp_list)
        ix_list.append(temp_list)
    print("当前全球IX数量为：", len(ix_list))
    save_path = "./ix.csv"
    write_to_csv(ix_list, save_path)

    """
    根据接入带宽新属性做二次分析
    1、统计全球各个国家所有IX总的接入带宽
    2、统计全球各大洲所有IX总的接入带宽
    """
    country_dict_speed = {}  # 国家IX总的接入带宽
    region_dict_speed = {}  # 大洲IX总的接入带宽

    for item in ix_list:
        item_country = item[7]
        item_region = item[8]
        item_speed = item[6]
        if item_country not in country_dict_speed.keys():
            country_dict_speed[item_country] = item_speed
        else:
            country_dict_speed[item_country] += item_speed

        if item_region not in region_dict_speed.keys():
            region_dict_speed[item_region] = item_speed
        else:
            region_dict_speed[item_region] += item_speed

    country_list_speed = []
    region_list_speed = []

    for key in country_dict_speed.keys():
        country_list_speed.append([key, country_dict_speed[key]])

    for key in region_dict_speed.keys():
        region_list_speed.append([key, region_dict_speed[key]])

    save_path = "./country_list_speed.csv"
    write_to_csv(country_list_speed, save_path)
    save_path = "./region_list_speed.csv"
    write_to_csv(region_list_speed, save_path)


if __name__ == "__main__":
    time_start = time.time()
    ix_crawler()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")