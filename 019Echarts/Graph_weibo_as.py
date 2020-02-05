# coding:utf-8
"""
create on Jan 6, 2020 By Wayne Yu

测试Graph-微博转发关系

"""
import json
import os
import random
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType


def read_as_info(file_name):
    """
    根据传入的as_core_map_data信息，读取as_info
    :param file_name:
    :return as_info:
    :return cn_as:
    """
    as_info = []
    cn_as = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    categories_list = []
    file_read = open(file_name, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split('|')
        categories_list.append(line[5])
        if line[5] == "RU":
            print(line)
            node_name = "AS" + str(line[0])
            node_size = int(line[1])

            if node_size > 42:
                # node_size = np.log((node_size / 4) + 10)
                node_size = np.log(node_size) * np.log(node_size)
                print(node_size)
            else:
                node_size = 8
            temp_dict["name"] = node_name
            temp_dict["symbolSize"] = node_size
            temp_dict["draggable"] = "True"
            temp_dict["value"] = line[1]
            temp_dict["category"] = line[5]

            cn_as.append(line[0])
            if int(line[1]) > 42:
                temp_dict_normal["show"] = "True"
                temp_dict_label["normal"] = temp_dict_normal
                temp_dict["label"] = temp_dict_label
                as_info.append(temp_dict)
                temp_dict = {}
                temp_dict_normal = {}
                temp_dict_label = {}
            else:
                as_info.append(temp_dict)
                temp_dict = {}

    categories_info = []
    for item in list(set(categories_list)):
        temp_dict["name"] = item
        categories_info.append(temp_dict)
        temp_dict = {}

    return as_info, cn_as, categories_info


def read_as_links(file_name, cn_as):
    """
    根据传入的as_rel和cn_as信息，读取as_links
    :param file_name:
    :param cn_as:
    :return as_links:
    """
    as_links= []
    temp_dict = {}
    file_read = open(file_name, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split('|')
        if line[0] in cn_as and line[1] in cn_as:
            # print(line)
            temp_dict["source"] = "AS"+str(line[0])
            temp_dict["target"] = "AS"+str(line[1])
            as_links.append(temp_dict)
            temp_dict = {}

    return as_links


def graph_weibo() -> Graph:
    with open(os.path.join("..\\000LocalData\\echart_example\\", "weibo.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories, cont, mid, userl = j
    as_info_dict, cn_as, categories_dict = read_as_info('..\\000LocalData\\as_compare\\as_core_map_data_integrate20191203.csv')
    print(as_info_dict)
    print(categories_dict)
    as_links_dict = read_as_links('..\\000LocalData\\as_compare\\as_rel_20191203_integrate.txt', cn_as)
    print(as_links_dict)
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="960px", page_title="Graph-俄罗斯AS网络互联关系图", theme=ThemeType.DARK))
        .add(
            "",
            as_info_dict,
            as_links_dict,
            categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=0.2,
            repulsion=100000,
            linestyle_opts=opts.LineStyleOpts(width=0.1),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Graph-俄罗斯AS网络互联关系图"),
        )
    )
    return c


graph_weibo().render("Graph_as_RU_circle.html")
