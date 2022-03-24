# coding:utf-8
"""
create on Mar 23, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

构建LINX事件前后，RU网络受到的影响比较

思路：
选取主要的几个IX（LINX、DE-CIX、AMS-IX），构建ix-net的连接关系网络图；
LINX事件发生后，绘制RU网络受到的影响，初步选择直接接入的网络，后续可以把下游网络也放进去。

启动http服务器，开启本地资源引用
 $ cd pyecharts-assets
 $ python -m http.server
 # Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
 # 默认会在本地 8000 端口启动一个文件服务器

"""
from pyecharts.globals import CurrentConfig
import json
import time
import csv

from pyecharts import options as opts
from pyecharts.charts import Graph
# from pyecharts.globals import ThemeType
import numpy as np
from pyecharts.datasets import register_files

CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/assets/v5/"
register_files({"ixTheme": ["themes/ixTheme", "js"]})

except_info_list = []  # 存储异常信息


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


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


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
    https://www.peeringdb.com/api/netixlan
    :return:
    """
    as2info = gain_as2info_pdb()
    ix2info = gain_ix2info_pdb()

    with open("../000LocalData/IXVis/netixlan.json") as json_file:
        html_json = json.load(json_file)
    ix_list = []  # 存储ix的信息（ix_id, name）
    as_list = []  # 存储as的信息（net_id, asn）
    ix_as_rel = []  # 存储ix和as的关系数据（ix_id, net_id, ix_name, asn）
    for item in html_json['data']:
        # print(item)
        """
        {'id': 38, 
        'net_id': 2, 
        'ix_id': 13, 
        'name': 'SIX Seattle: MTU 1500', 
        'ixlan_id': 13, 
        'notes': '', 
        'speed': 200000, 
        'asn': 20940, 
        'ipaddr4': '206.81.80.113', 
        'ipaddr6': '2001:504:16::51cc', 
        'is_rs_peer': False, 
        'operational': True, 
        'created': '2010-07-29T00:00:00Z', 
        'updated': '2020-02-12T14:34:55Z', 
        'status': 'ok'}
        基于IX NAME构建主要IX的接入关系
        """
        if item['name'].find("LINX") == -1 and \
                item['name'].find("DE-CIX") == -1 and \
                item['name'].find("AMS-IX") == -1 and \
                item['name'].find("MSK-IX") == -1:
            continue

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
        # print(ix_str, "- - - ", as_str)
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
    save_path = "../000LocalData/RU&UA/IXVis/ix_as_rel.csv"
    write_to_csv(ix_as_rel, save_path)

    save_path = "../000LocalData/RU&UA/IXVis/ix_list_new.csv"
    write_to_csv(ix_list_new, save_path)
    save_path = "../000LocalData/RU&UA/IXVis/as_list_new.csv"
    write_to_csv(as_list_new, save_path)
    save_path = "../000LocalData/RU&UA/IXVis/ix_as_rel_new.csv"
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
    as2country_dict = gain_as2country_caida()

    ix_list, as_list, ix_as_rel, weight_dic_ix, weight_dic_as = generate_ix_rel()
    type_group = ["AS(RU)", "IX", "AS(非RU)"]

    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    categories_list = []

    node_info = []
    node_list = []

    # 处理node AS的信息
    for item in as_list:
        item_country = "ZZ"
        try:
            item_country = as2country_dict[str(item[1])]
        except Exception as e:
            except_info_list.append(e)

        categories_str = "AS(非RU)"
        if item_country == "RU":
            categories_str = "AS(RU)"

        categories_list.append(categories_str)
        node_name = "AS" + str(item[1]) + "-" + str(item[2])
        node_list.append(node_name)
        try:
            node_size = np.sqrt(int(weight_dic_as[node_name])) + 2
        except Exception as e:
            print(e)
            node_size = 4

        temp_dict["name"] = node_name
        temp_dict["symbolSize"] = node_size
        temp_dict["symbol"] = "circle"
        temp_dict["draggable"] = "False"
        temp_dict["value"] = "<AS" + str(item[1]) + ">" + str(item[2])
        temp_dict["category"] = categories_str

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

        if int(weight_dic_ix[node_name]) > 100:
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
    with open("../000LocalData/RU&UA/IXVis/ix_as.json", 'w') as f:
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
                                      theme="ixTheme"))
        .add(
            "Circle is AS, and rectangle is IX.",
            node_info,
            links,
            categories_info,
            is_selected=True,  # 是否选中图例
            is_focusnode=False,  # 是否在鼠标移动到节点的时候突出显示节点及节点的边和邻接节点
            is_roam=True,  # 是否开启鼠标缩放和平移漫游
            is_draggable=True,  # 节点是否可拖拽
            is_rotate_label=False,  # 是否旋转标签
            layout="force",  # 图布局模式，none(使用xy坐标)，circular, force
            # symbol="rect",  # Echarts提供的标记包括circle, rect, roundRect, triangle, diamond, pin ,arrow
            edge_length=50,  # 节点之间距离
            gravity=0.2,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(width=0.2, opacity=0.8, color='target', curve=0.2),
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
    opt_title_name = "Graph-IX星云图可视化"
    draw_rel(opt_title_name).render("../000LocalData/RU&UA/IXVis/global_ix_new.html")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
