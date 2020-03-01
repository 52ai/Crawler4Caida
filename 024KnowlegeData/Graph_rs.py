# coding:utf-8
"""
create on Feb 17, 2020 By Wayne Yu

绘制院软课题知识网络拓扑图

"""
import json
import os
import random
import time
from urllib.request import urlopen

from pyecharts import options as opts
from pyecharts.charts import Graph, Page, Tab
from pyecharts.globals import ThemeType
from pyecharts.components import Table


def list2dict_count(res_list):
    """
    根据传入的list，统计各元素的频次，并返回频次字典
    :param res_list:
    :return des_dict:
    """
    des_dict = {}
    for item in set(res_list):
        des_dict[item] = 0
    for item in res_list:
        des_dict[item] += 1
    return des_dict


def dict2list_rank(res_dict):
    """
    根据传入的dict，将其转换为list，并按降序排名
    :param res_dict:
    :return des_list:
    """
    des_list = []
    temp_list = []
    for key in res_dict.keys():
        temp_list.append(key)
        temp_list.append(res_dict[key])
        des_list.append(temp_list)
        temp_list = []
    des_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    return des_list


def graph_rs(year_string, opts_title_name) -> Graph:
    with open(os.path.join("..\\000LocalData\\echart_example\\", "weibo.json"), "r", encoding="utf-8") as f:
        j = json.load(f)
        nodes, links, categories, cont, mid, userl = j
    # print(nodes)
    # print(links)
    # print(categories)

    # print(hjson["type"])
    # print(hjson["categories"])
    # print(hjson["nodes"])
    # print(hjson["links"])
    nodes_list, links_list, categories_list, title_string = generate_json(year_string)

    opts_title_name = opts_title_name + title_string
    c = (
        Graph(init_opts=opts.InitOpts(width="1920px", height="900px", page_title=opts_title_name, theme=ThemeType.INFOGRAPHIC))
        .add(
            "",
            nodes_list,
            links_list,
            categories_list,
            # layout="circular",
            is_rotate_label=True,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(width=0.1, color="source", curve=0),
            label_opts=opts.LabelOpts(position="right", font_size=12),
            # label_opts=opts.LabelOpts(is_show=True),
            edge_label=opts.LabelOpts(
                is_show=False,
                position="middle",
                # formatter=""
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=opts_title_name),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="2%",
                pos_top="20%",
            )
        )
    )
    return c


def generate_json(year_string):
    """
    生成绘制拓扑图所需要的参数
    :return:
    """
    res_file = "..\\000LocalData\\caict_k\\research_subject_intergrate.csv"
    res_file_read = open(res_file, 'r', encoding='utf-8')
    res_list = []
    res_name_list = []
    for line in res_file_read.readlines():
        line = line.strip().split("|")
        line[1] = line[1].replace("--", "-", 10)
        # if line[2] in ["2019", "2018", "2017"]:
        if line[2] == year_string:
            if line[1] not in res_name_list:
                res_list.append(line)
                # print(line[8])
                res_name_list.append(line[1])
    print("处理完成的程序采集信息记录数：", len(res_list))
    print("是否存在重名：", len(res_name_list), len(list(set(res_name_list))))
    title_string = "（Nodes："+str(len(res_list))+"个）"
    # 生成nodes信息
    nodes_list = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    for item in res_list:
        temp_dict["name"] = item[1] + "(" + item[8] + ")"
        temp_dict["draggable"] = True
        temp_dict["value"] = len(item[8].strip().split("、"))
        temp_dict["symbolSize"] = 12
        temp_dict["category"] = item[6]

        temp_dict_normal["show"] = False
        temp_dict_label["normal"] = temp_dict_normal
        temp_dict["label"] = temp_dict_label
        nodes_list.append(temp_dict)
        temp_dict = {}
        temp_dict_normal = {}
        temp_dict_label = {}

    # print(nodes_list)
    # for item in nodes_list:
    #     print(item)
    # 生成links信息
    links_list = []
    temp_dict = {}
    iter_cnt_out = 0
    key_words_list = []  # 存储关键词
    for item_out in res_list:
        key_words_list.extend(item_out[8].strip().split("、"))
        key_words_list_out = item_out[8].strip().split("、")
        # iter_cnt_in = iter_cnt_out + 1
        iter_cnt_in = 0
        for item_in in res_list[iter_cnt_in:]:
            key_words_list_in = item_in[8].strip().split("、")
            # 如果关键词存在重合，则存在连边
            if len(list(set(key_words_list_out) & set(key_words_list_in))) != 0:
            # if item_out[6] == item_in[6]:
            # if item_out[4] == item_in[4]:
            #     print(key_words_list_out)
            #     print(key_words_list_in)
            #     print()
                temp_dict["source"] = item_out[1] + "(" + item_out[8] + ")"
                temp_dict["target"] = item_in[1] + "(" + item_in[8] + ")"
                temp_dict["value"] = len(list(set(key_words_list_out) & set(key_words_list_in)))
                links_list.append(temp_dict)
                temp_dict = {}
            else:
                # print("不存在关键词重合")
                pass
            iter_cnt_in += 1
        iter_cnt_out += 1
    # print(set(key_words_list))
    # print(links_list)
    # for item in links_list:
    #     print(item)
    # 生成categories信息
    categories_type = ['大数据与人工智能', '两化融合与产业互联网', '无线移动', '网络安全与国际治理', '信息网络', '数字经济与法律监管', 'ICT', '先进计算']
    categories_temp_list = []
    for item in res_list:
        categories_temp_list.append(item[6])
    categories_rank_list = dict2list_rank(list2dict_count(categories_temp_list))
    print(categories_rank_list)
    categories_list = []
    temp_dict = {}
    for item_type in categories_type:
        temp_dict["name"] = item_type
        categories_list.append(temp_dict)
        temp_dict = {}
    # print(categories_list)
    return nodes_list, links_list, categories_list, title_string


def table_base()->Table:
    table = Table()
    heardes = ["课题名称", "课题编号", "年份", "负责人", "负责单位", "课题类型", "领域", "课题方向", "关键词", "URL"]
    res_file = "..\\000LocalData\\caict_k\\research_subject_intergrate.csv"
    res_file_read = open(res_file, 'r', encoding='utf-8')
    res_list = []
    temp_list = []
    res_name_list = []
    for line in res_file_read.readlines():
        line = line.strip().split("|")
        if line[1] not in res_name_list:
            temp_list.append(line[0])
            temp_list.append(line[1].replace("--", "-", 10))
            temp_list.append(line[2])
            temp_list.append(line[3])
            temp_list.append(line[4])
            temp_list.append(line[5])
            temp_list.append(line[6])
            temp_list.append(line[7])
            temp_list.append(line[8])
            temp_list.append(line[10])
            # print(temp_list)
            res_list.append(temp_list)
            temp_list = []
            res_name_list.append(line[1])
    table.add(heardes, res_list).set_global_opts(
        title_opts=opts.ComponentTitleOpts(title="院软课题知识数据表（2010-2019）")
    )
    return table


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # generate_json()
    # year_str = "2014"
    # opts_title = year_str + "年院软课题知识网络拓扑图绘制"
    # graph_rs(year_str, opts_title).render("..\\000LocalData\\caict_k\\Graph_rs_render.html")
    # 开始尝试tab选项卡多图的展示
    tab = Tab(page_title="院软课题知识网络拓扑图绘制(2010-2019)")
    for year_item in range(2019, 2009, -1):
        opts_title = str(year_item) + "年院软课题知识网络拓扑图绘制"
        tab.add(graph_rs(str(year_item), opts_title), str(year_item)+"年")
    tab.add(table_base(), "数据查询表")
    tab.render("..\\000LocalData\\caict_k\\CAICT_rs_graph_force.html")
    time_end = time.time()  # 记录程序结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


""""
cnzz

<script type="text/javascript">var cnzz_protocol = (("https:" == document.location.protocol) ? "https://" : "http://");document.write(unescape("%3Cspan id='cnzz_stat_icon_4586080'%3E%3C/span%3E%3Cscript src='" + cnzz_protocol + "s11.cnzz.com/stat.php%3Fid%3D4586080%26show%3Dpic2' type='text/javascript'%3E%3C/script%3E"));</script>

"""