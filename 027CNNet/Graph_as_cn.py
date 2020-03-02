# coding:utf-8
"""
create on Feb 21, 2020 By Wayne Yu

绘制中国AS互联关系

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
        categories_list.append(line[-1])
        if line[-1] == "CN":  # 判断国家
            cn_as.append(line[0])
            # print(line)
            node_name = "AS" + str(line[0])
            node_size = np.sqrt(int(line[2])/10)
            # if node_size > 42:
            #     # node_size = np.log((node_size / 4) + 10)
            #     node_size = np.log(node_size) * np.log(node_size)
            #     # print(node_size)
            # else:
            #     node_size = 2
            temp_dict["name"] = node_name
            temp_dict["symbolSize"] = node_size
            temp_dict["draggable"] = "True"
            temp_dict["value"] = line[2]
            temp_dict["category"] = line[-1]

            if int(line[2]) > 420000000000:
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
    as_links = []
    temp_dict = {}
    file_read = open(file_name, 'r', encoding='utf-8')
    iter_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        if line[0] in cn_as and line[1] in cn_as:
            # print(line)
            temp_dict["source"] = "AS"+str(line[0])
            temp_dict["target"] = "AS"+str(line[1])
            as_links.append(temp_dict)
            temp_dict = {}
            iter_cnt += 1
    # print("iter_cnt:", iter_cnt)
    return as_links


def graph_weibo(title_name) -> Graph:
    # file_in = '..\\000LocalData\\as_cn\\as_map_caida_20200221_cn.csv'
    # bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\20200201.as-rel.txt"

    file_in = '..\\000LocalData\\as_cn\\as_map_gao_20200221_cn.csv'
    bgp_file = "..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt"
    as_info_dict, cn_as, categories_dict = read_as_info(file_in)
    print("nodes:", len(as_info_dict))
    print("categories:", len(categories_dict))
    print("cn as:", len(cn_as))
    as_links_dict = read_as_links(bgp_file, cn_as)
    print("links:", len(as_links_dict))

    out_json = {}
    out_json["nodes"] = as_info_dict
    out_json["links"] = as_links_dict
    out_json["categories"] = categories_dict
    print(out_json)
    final_json = json.dumps(out_json, indent=4)
    with open("..\\000LocalData\\as_cn\\graph_cn_gao.json", 'a') as f:
        f.write(final_json)

    title_name = title_name + "[Nodes:" + str(len(as_info_dict)) + " Links:" + str(len(as_links_dict)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="960px", page_title=title_name, theme=ThemeType.DARK))
        .add(
            "",
            as_info_dict,
            as_links_dict,
            categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=0.2,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(width=0.1, opacity=0.3, color='#fff', curve=0),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=title_name),
        )
    )
    return c


opt_title_name = "Graph-中国AS网络互联关系拓扑图（2020-Gao）"
graph_weibo(opt_title_name).render("..\\000LocalData\\as_cn\\graph_cn_gao.html")
