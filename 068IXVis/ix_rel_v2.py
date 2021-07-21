# coding:utf-8
"""
create on July 4, 2021 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

抽取交换中心到网络间的关系，以供星云图绘制使用

思路：
直接通过https://www.peeringdb.com/api/netixlan
抽取ix和net的对应关系，即每个ix都有哪些网络接入

形成ix组，net组，以及ix-net的关系

V2:
在第一版的基础上，新增ix和net的权重属性，并以此来确定节点的大小

李博士提出修改建议：

1、标注出大型网络的AS
2、研究这里面有多少个独立的AS，以及占全球的比例（说明一个交换中心的通达情况）
3、未来进一步可从图中去掉Tier-1、Tier-2网络，研究交换中心到全球网络的可达性
4、某个国家的网络通过交换中心实现外部可达等情况


"""
from urllib.request import urlopen
import json
from datetime import *
import time
import csv

from pyecharts import options as opts
from pyecharts.charts import Graph, Page
from pyecharts.globals import ThemeType
import numpy as np


as_info_file = '../000LocalData/as_Gao/asn_info.txt'


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
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


def gain_as2info_pdb():
    """
    根据pdb的数据获取as 2 info的信息
    https://www.peeringdb.com/api/net
    :return as2info:
    """
    with open("../000LocalData/IXVis/net.json") as json_file:
        html_json = json.load(json_file)
    as2info = {}  # as2info的字典
    for item in html_json['data']:
        asn = item["asn"]
        name = item["name"]
        if asn not in as2info.keys():
            as2info[asn] = name
    # print("NET原始信息记录：", len(html_json['data']))
    print("AS信息字典记录：", len(as2info.keys()))
    return as2info


def gain_ix2info_pdb():
    """
    根据pdb的数据获取ix 2 info的信息
    https://www.peeringdb.com/api/ix
    :return ix2info:
    """
    with open("../000LocalData/IXVis/ix.json") as json_file:
        html_json = json.load(json_file)
    ix2info = {}  # ix2info的字典
    for item in html_json['data']:
        ix_id = item['id']
        ix_name = item['name']
        ix_name_long = item['name_long']
        city = item['city']
        country = item['country']
        region = item['region_continent']
        net_count = item['net_count']
        fac_count = item['fac_count']
        if ix_id not in ix2info.keys():
            ix2info[ix_id] = [ix_name, ix_name_long, city, country, region, net_count, fac_count]
    # print("IX原始信息记录表：", len(html_json['data']))
    print("IX信息字典记录：", len(ix2info.keys()))
    return ix2info


def generate_ix_rel():
    """
    基于PEERING DB数据抽取ix和net的对应关系
    :return:
    """
    # as2country, as2info = gain_as2country()
    as2info = gain_as2info_pdb()
    ix2info = gain_ix2info_pdb()

    # html = urlopen(r"https://www.peeringdb.com/api/netixlan")
    # html_json = json.loads(html.read())
    with open("../000LocalData/IXVis/netixlan.json") as json_file:
        html_json = json.load(json_file)
    ix_list = []  # 存储ix的信息（ix_id, name）
    as_list = []  # 存储as的信息（net_id, asn）
    ix_as_rel = []  # 存储ix和as的关系数据（ix_id, net_id, ix_name, asn）
    for item in html_json['data']:
        # print(item)
        ix_id = item['ix_id']
        ix_name = item['name'].strip().split(":")[0]
        try:
            ix_str = ix2info[ix_id][1]
        except Exception as e:
            print(e)
            ix_str = "UNKnow"

        net_id = item['net_id']
        asn = item['asn']
        try:
            asn_str = as2info[asn]
        except Exception as e:
            print(e)
            asn_str = "UNKnow"

        if [ix_id, ix_name] not in ix_list:
            ix_list.append([ix_id, ix_name])
        if [net_id, asn, asn_str] not in as_list:
            as_list.append([net_id, asn, asn_str])
        if [ix_id, net_id, ix_name, asn, ix_str, asn_str] not in ix_as_rel:
            ix_as_rel.append([ix_id, net_id, ix_name, asn, ix_str, asn_str])

    """
    根据生成的ix和as的关系数据，构建ix和as的权重
    """
    ix_as_rel_new = []  # 存储新的关系列表
    weight_dic_ix = {}  # 存储节点key和其度value
    weight_dic_as = {}  # 存储节点key和其度value
    for item in ix_as_rel:
        ix_str = "IX" + str(item[0]) + "-" + str(item[2])
        as_str = "AS" + str(item[3]) + "-" + str(item[5])
        print(ix_str, "- - - ", as_str)
        ix_as_rel_new.append([ix_str, as_str])
        if ix_str not in weight_dic_ix.keys():
            weight_dic_ix[ix_str] = 1
        else:
            weight_dic_ix[ix_str] += 1

        if as_str not in weight_dic_as.keys():
            weight_dic_as[as_str] = 1
        else:
            weight_dic_as[as_str] += 1

    """
    补全ix_list和as_list
    """
    ix_list_new = []
    for item in ix_list:
        ix_str = "IX" + str(item[0]) + "-" + str(item[1])
        try:
            ix_str_degree = weight_dic_ix[ix_str]
        except Exception as e:
            print(e)
            ix_str_degree = 0
        item.append(ix_str_degree)
        ix_list_new.append(item)

    as_list_new = []
    for item in as_list:
        as_str = "AS" + str(item[1]) + "-" + str(item[2])
        try:
            as_str_degree = weight_dic_as[as_str]
        except Exception as e:
            print(e)
            as_str_degree = 0
        item.append(as_str_degree)
        as_list_new.append(item)

    # 数据持久化
    save_path = "../000LocalData/IXVis/ix_as_rel.csv"
    write_to_csv(ix_as_rel, save_path)

    save_path = "../000LocalData/IXVis/ix_list_new.csv"
    write_to_csv(ix_list_new, save_path)
    save_path = "../000LocalData/IXVis/as_list_new.csv"
    write_to_csv(as_list_new, save_path)
    save_path = "../000LocalData/IXVis/ix_as_rel_new.csv"
    write_to_csv(ix_as_rel_new, save_path)

    print("IX-AS边的总记录:", len(html_json['data']))
    print("IX记录数:", len(ix_list))
    print("AS记录数:", len(as_list), "占全球自治域网络：", len(as_list)/70000)
    print("IX-AS关系数量（数据处理后）:", len(ix_as_rel_new))

    return ix_list, as_list, ix_as_rel_new, weight_dic_ix, weight_dic_as


def generate_draw_json():
    """
    根据处理的全球IX数据生成绘图用的json数据
    :return:
    """
    ix_list, as_list, ix_as_rel, weight_dic_ix, weight_dic_as = generate_ix_rel()
    type_group = ["AS", "IX"]

    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    categories_list = []

    node_info = []
    node_list = []

    # 处理node AS的信息
    for item in as_list:
        categories_list.append("AS")
        node_name = "AS" + str(item[1]) + "-" + str(item[2])
        node_list.append(node_name)
        try:
            node_size = np.sqrt(int(weight_dic_as[node_name])) + 2
        except Exception as e:
            print(e)
            node_size = 2
        temp_dict["name"] = node_name
        temp_dict["symbolSize"] = node_size
        temp_dict["symbol"] = "circle"
        temp_dict["draggable"] = "False"
        temp_dict["value"] = "<AS" + str(item[1]) + ">" + str(item[2])
        temp_dict["category"] = "AS"

        if int(weight_dic_as[node_name]) > 190:
            temp_dict_normal["show"] = "True"
            temp_dict_normal["color"] = "yellow"
            temp_dict_normal["font_size"] = 8
            temp_dict_normal["font_style"] = "oblique"
            temp_dict_normal["font_weight"] = "bold"
            temp_dict_normal["rotate"] = 45
            temp_dict_normal["margin"] = 0  # 刻度标签与轴线之间的距离
            temp_dict_label["normal"] = temp_dict_normal
            temp_dict["label"] = temp_dict_label
            node_info.append(temp_dict)
            temp_dict = {}
            temp_dict_normal = {}
            temp_dict_label = {}
        else:
            node_info.append(temp_dict)
            temp_dict = {}

    # 处理node IX的信息
    for item in ix_list:
        categories_list.append("IX")
        node_name = "IX" + str(item[0]) + "-" + str(item[1])
        node_list.append(node_name)
        try:
            node_size = np.sqrt(int(weight_dic_ix[node_name])) + 4.8
        except Exception as e:
            print(e)
            node_size = 4.8
        temp_dict["name"] = node_name
        temp_dict["symbolSize"] = node_size
        temp_dict["symbol"] = "rect"
        temp_dict["draggable"] = "False"
        temp_dict["value"] = "<IX>" + str(item[1])
        temp_dict["category"] = "IX"

        if int(weight_dic_ix[node_name]) > 420:
            temp_dict_normal["show"] = "True"
            temp_dict_label["normal"] = temp_dict_normal
            temp_dict["label"] = temp_dict_label
            node_info.append(temp_dict)
            temp_dict = {}
            temp_dict_normal = {}
            temp_dict_label = {}
        else:
            node_info.append(temp_dict)
            temp_dict = {}

    categories_list = type_group
    categories_info = []
    for item in categories_list:
        temp_dict["name"] = item
        categories_info.append(temp_dict)
        temp_dict = {}

    print("全部节点信息：", len(node_info))
    # print("全部记录:", len(node_list))
    print("Categories:", len(categories_info))
    """
    处理边的关系
    """
    links = []
    temp_dict = {}
    for item in ix_as_rel:
        temp_dict["source"] = str(item[0])
        temp_dict["target"] = str(item[1])
        links.append(temp_dict)
        temp_dict = {}
    print("全部关系记录：", len(links))

    out_json = list()
    out_json.append(node_info)
    out_json.append(links)
    out_json.append(categories_info)
    final_json = json.dumps(out_json, indent=4)
    with open("../000LocalData/IXVis/ix_as.json", 'w') as f:
        f.write(final_json)

    return node_info, links, categories_info


def draw_rel(title_name) -> Graph:
    """
    根据处理的全球IX json数据，绘制星云图
    :return:
    """
    node_info, links, categories_info = generate_draw_json()

    title_name = title_name + "[Nodes:" + str(len(node_info)) + " Links:" + str(len(links)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="1900px",
                                      height="900px",
                                      page_title=title_name,
                                      theme=ThemeType.DARK))
        .add(
            "Circle is AS, and rectangle is IX.",
            node_info,
            links,
            categories_info,
            is_selected=True,  # 是否选中图例
            is_focusnode=False,  # 是否在鼠标移动到节点的时候突出显示节点及节点的边和邻接节点
            is_roam=True,  # 是否开启鼠标缩放和平移漫游
            is_draggable=False,  # 节点是否可拖拽
            is_rotate_label=False,  # 是否旋转标签
            layout="force",  # 图布局模式，none(使用xy坐标)，circular, force
            # symbol="rect",  # Echarts提供的标记包括circle, rect, roundRect, triangle, diamond, pin ,arrow
            edge_length=50,  # 节点之间距离
            gravity=0.2,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(width=0.2, opacity=0.8, color='source', curve=0.2),
            label_opts=opts.LabelOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True)
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title=title_name,
                                      title_textstyle_opts=opts.TextStyleOpts(color="#fff"),
                                      pos_left="2%"),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="2%",
                pos_top="5%",
                pos_bottom="5",
                textstyle_opts=opts.TextStyleOpts(color="#fff")
            )
        )
    )
    return c


if __name__ == "__main__":
    time_start = time.time()
    # generate_ix_rel()
    # generate_draw_json()
    opt_title_name = "Graph-全球IX星云图可视化"
    draw_rel(opt_title_name).render("../000LocalData/IXVis/global_ix_new.html")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")



