# coding:utf-8
"""
create on May 17, 2020 By Wayne Yu

绘制全球AS网络互联关系-星云图，用于院大屏展示系统

"""
import json
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType


def read_as_info(file_name):
    """
    根据传入的as_core_map_data信息，读取as_info
    :param file_name:
    :return as_info:
    :return cn_as:
    """
    as_info = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    categories_list = []
    file_read = open(file_name, 'r', encoding='utf-8')
    as_list = []
    # 中日韩
    country_group = ["CN", "JP", "KR", "Others"]
    # 中国-东盟10国文莱（BN）、柬埔寨（KH）、印度尼西亚（ID）、老挝（LA）、马来西亚（MY）、缅甸（MM）、菲律宾(PH)、新加坡(SG)、泰国(TH)、越南(VN)
    # country_group = ["CN", "BN", "KH", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "VN"]

    for line in file_read.readlines():
        line = line.strip().split('|')
        # print(line)
        if line[8] in country_group:
            # categories_list.append(line[8])  # 添加分类
            as_list.append(line[0])
            node_name = "AS" + str(line[0])
            node_size = np.sqrt(int(line[1]))
            temp_dict["name"] = node_name
            temp_dict["symbolSize"] = node_size
            temp_dict["draggable"] = "True"
            temp_dict["value"] = line[1]
            temp_dict["category"] = line[8]

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
        else:
            # categories_list.append("Others")  # 添加分类
            as_list.append(line[0])
            node_name = "AS" + str(line[0])
            node_size = np.sqrt(int(line[1]))
            temp_dict["name"] = node_name
            temp_dict["symbolSize"] = node_size
            temp_dict["draggable"] = "True"
            temp_dict["value"] = line[1]
            temp_dict["category"] = "Others"

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

    categories_list = country_group
    categories_info = []
    # for item in list(set(categories_list)):
    #     temp_dict["name"] = item
    #     categories_info.append(temp_dict)
    #     temp_dict = {}
    for item in categories_list:
        temp_dict["name"] = item
        categories_info.append(temp_dict)
        temp_dict = {}

    return as_info, as_list, categories_info


def read_as_links(file_name, as_list):
    """
    根据传入的as_rel和cn_as信息，读取as_links
    :param file_name:
    :param cn_as:
    :return as_links:
    """
    # print(as_list)
    as_links = []
    temp_dict = {}
    file_read = open(file_name, 'r', encoding='utf-8')
    iter_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        if line[0] in as_list and line[1] in as_list:
            temp_dict["source"] = "AS"+str(line[0])
            temp_dict["target"] = "AS"+str(line[1])
            as_links.append(temp_dict)
            temp_dict = {}
        iter_cnt += 1
    return as_links


def graph_weibo(title_name) -> Graph:
    # file_in = '..\\000LocalData\\as_cn\\as_map_caida_20200221_cn.csv'
    # bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\20200201.as-rel.txt"

    file_in = '..\\000LocalData\\as_map\\as_core_map_data_new19980101.csv'
    bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\19980101.as-rel.txt"

    # file_in = '..\\000LocalData\\as_cn\\as_map_gao_20200221.csv'
    # bgp_file = "..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt"
    as_info_dict, as_list, categories_dict = read_as_info(file_in)
    print("nodes:", len(as_info_dict))
    print("categories:", len(categories_dict))
    print("as list:", len(as_list))
    as_links_dict = read_as_links(bgp_file, as_list)
    print("links:", len(as_links_dict))

    out_json = []
    out_json.append(as_info_dict)
    out_json.append(as_links_dict)
    out_json.append(categories_dict)
    # print(out_json)
    final_json = json.dumps(out_json, indent=4)
    with open("..\\000LocalData\\caict_display\\graph_global_display.json", 'a') as f:
        f.write(final_json)

    title_name = title_name + "[Nodes:" + str(len(as_info_dict)) + " Links:" + str(len(as_links_dict)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="3743px", height="1594px", page_title=title_name, theme=ThemeType.DARK))
        .add(
            "",
            as_info_dict,
            as_links_dict,
            categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=0.2,
            repulsion=420,
            linestyle_opts=opts.LineStyleOpts(width=0.1, opacity=0.8, color='source', curve=0),
            label_opts=opts.LabelOpts(is_show=False, font_size=15),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                textstyle_opts=opts.TextStyleOpts(font_size=28),
                item_height=28,
                item_width=50),
            title_opts=opts.TitleOpts(title=title_name,
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=36),
                                      ),
        )
    )
    return c


opt_title_name = "Graph-全球AS网络互联关系拓扑图（1998）"
graph_weibo(opt_title_name).render("..\\000LocalData\\caict_display\\graph_global_dispaly.html")
