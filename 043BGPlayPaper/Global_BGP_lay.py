# coding:utf-8
"""
create on June 9, 2020 By Wayne Yu

重新考虑全球BGP互联拓扑图的Layout
有两个目的，其一，地图基础课题第二篇论文输出绘图案例的精选及优化；其二，大屏展示系统星云图界面的优化。

三个可能的优化的方向

1）舍去连线，参考The Internet Mao的形式，绘制全球AS级网络互联关系地图
2）研究机器学习聚类算法，寻找合适的聚类模式，或者改进之
3）提前输出点的静态坐标，再行绘制降低实时计算量

"""
import json
import numpy as np

from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import ThemeType
import time


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
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as_info():
    """
    获取AS的相关信息
    :return as_info_dict:
    """
    as_info_file_gao = '../000LocalData/as_Gao/asn_info.txt'
    as_info_dict = {}  # 存储AS信息的字典
    file_read = open(as_info_file_gao, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_info_dict[line[0]] = line[-1].split(',')[-1]

    return as_info_dict


def gain_country_info():
    """
    根据国家的缩写，翻译为中文
    :return country_info_dict:
    """
    geo_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'
    coutry_info_dict = {}
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        coutry_info_dict[line[4]] = line[5]
    return coutry_info_dict


def read_as_info(file_name, as2country):
    """
    根据传入的as_core_map_data信息，读取as_info
    :param file_name:
    :param as2country:
    :return as_info:
    :return cn_as:
    """
    as_info = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    file_read = open(file_name, 'r', encoding='utf-8')
    as_list = []  # 记录所有展示的as列表
    country_group = ["中国", "日本", "俄罗斯", "香港"]
    for line in file_read.readlines():
        line = line.strip().split('|')
        try:
            country_cn = country_en2cn[line[8]].strip("\"")
            # print(country_cn)
        except Exception as e:
            print(e)
            continue
        if country_cn in country_group:
            as_list.append(line[0])
            node_name = "AS" + str(line[0])
            node_size = np.sqrt(int(line[1]))
            temp_dict["name"] = node_name
            temp_dict["symbolSize"] = node_size
            temp_dict["draggable"] = "True"
            temp_dict["value"] = line[1]
            temp_dict["category"] = country_cn

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


def graph_as_lay(title_name, country_en2cn, time_str) -> Graph:
    file_in = '..\\000LocalData\\as_map\\as_core_map_data_new' + time_str + '1001.csv'
    bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\" + time_str + "1001.as-rel.txt"
    as_info_dict, as_list, categories_dict = read_as_info(file_in, country_en2cn)
    print("Nodes:", len(as_info_dict))
    print("Categories:", len(categories_dict))
    print("As List:", len(as_list))
    as_links_dict = read_as_links(bgp_file, as_list)
    print("links:", len(as_links_dict))
    out_json = []
    out_json.append(as_info_dict)
    out_json.append(as_links_dict)
    out_json.append(categories_dict)
    # print(out_json)
    final_json = json.dumps(out_json, indent=4)
    with open("..\\000LocalData\\BGPlay\\Global_BGP_lay.json", 'a') as f:
        f.write(final_json)

    title_name = title_name + "[Nodes:" + str(len(as_info_dict)) + " Links:" + str(len(as_links_dict)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="1000px", height="691.883px", page_title=title_name, theme=ThemeType.DARK, bg_color="#000"))
        .add(
            "",
            as_info_dict,
            as_links_dict,
            categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=0.15,
            repulsion=42,
            linestyle_opts=opts.LineStyleOpts(width=0.5, opacity=0.3, color='source', curve=0),
            label_opts=opts.LabelOpts(is_show=False, font_size=8),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=14))
                   )
        )
    return c


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    time_str = "1999"
    country_en2cn = gain_country_info()
    opt_title_name = "Graph-全球AS网络互联关系拓扑图"
    graph_as_lay(opt_title_name, country_en2cn, time_str).render("..\\000LocalData\\BGPlay\\Global_BGP_lay.html")
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

