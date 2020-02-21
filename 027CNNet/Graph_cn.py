# coding: utf-8
"""
create on Feb 21, 2020 By Wayne YU

Version:1.0
Description:

在多数据源中国AS网络画像构建基础之上，开始绘制中国AS网络互联拓扑图（亦可星云图）

"""

import openpyxl
import csv
import time
from urllib.request import urlopen
import json
from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
import numpy as np


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def graph_topology(res_json, opts_title_name)->Graph:
    """
    绘制网络拓扑图
    :param res_json:
    :param opts_title_name:
    :return:
    """
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="960px", page_title=opts_title_name, theme=ThemeType.SHINE))
        .add(
            "",
            res_json["nodes"],
            res_json["links"],
            res_json["categories"],
            # layout="circular",
            is_rotate_label=True,
            gravity=5,
            repulsion=100000,
            linestyle_opts=opts.LineStyleOpts(width=0.2),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=opts_title_name),
        )
    )
    return c


def generate_json(as_map_file, as_rel_file):
    """
    根据AS网络用户画像及as 互联关系数据生成绘图json数据
    :param as_map_file:
    :param as_rel_file:
    :return re_json:
    """
    re_json = {}
    # 生成categories
    catergories_list = []
    # 生成nodes
    as_map_file_read = open(as_map_file, 'r', encoding='utf-8')
    nodes_list = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    internal_as_list = []
    for item in as_map_file_read.readlines():
        item = item.strip().split("|")
        # print(item)
        internal_as_list.append(item[0])  # 构建内部AS 列表
        temp_dict["name"] = item[0]
        temp_dict["draggable"] = True
        temp_dict["value"] = item[2]
        if int(item[2]) <= 10:
            temp_dict["symbolSize"] = 10
        else:
            temp_dict["symbolSize"] = int(item[2])+1
        # temp_dict["symbolSize"] = np.log(int(item[2])+1)
        # temp_dict["category"] = 0

        temp_dict_normal["show"] = False
        temp_dict_label["normal"] = temp_dict_normal
        temp_dict["label"] = temp_dict_label
        nodes_list.append(temp_dict)
        temp_dict = {}
        temp_dict_normal = {}
        temp_dict_label = {}
    print("Internal AS List:", len(internal_as_list))
    # print(nodes_list)
    # 生成links信息
    as_rel_file_read = open(as_rel_file, 'r', encoding='utf-8')
    links_list = []
    temp_dict = {}
    for line in as_rel_file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        # print(line)
        try:
            if line[0] in internal_as_list and line[1] in internal_as_list:
                temp_dict["source"] = line[0]
                temp_dict["target"] = line[1]
                temp_dict["value"] = 1
                links_list.append(temp_dict)
                temp_dict = {}
        except Exception as e:
            print("ERROR", e)
    print(len(links_list))
    # print(links_list)
    re_json['categories'] = catergories_list
    re_json['nodes'] = nodes_list
    re_json['links'] = links_list
    return re_json


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    as_map_caida_file = '..\\000LocalData\\as_cn\\as_map_gao_20200221_cn.csv'
    rel_file_caida = "..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt"
    re_json = generate_json(as_map_caida_file, rel_file_caida)
    graph_topology(re_json, "中国AS网络拓扑图").render("..\\000LocalData\\as_cn\\graph_cn.html")
    time_end = time.time()  # 记录程序结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")