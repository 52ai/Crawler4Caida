# coding:utf-8
"""
create on June 9, 2020 By Wayne Yu

重新考虑全球BGP互联拓扑图的Layout
有两个目的，其一，地图基础课题第二篇论文输出绘图案例的精选及优化；其二，大屏展示系统星云图界面的优化。

三个可能的优化的方向

1）舍去连线，参考The Internet Map的形式，绘制全球AS级网络互联关系地图
2）研究机器学习聚类算法，寻找合适的聚类模式，或者改进之
3）提前输出点的静态坐标，再行绘制降低实时计算量

*********************实验记录*********************
实践是检验真理的唯一标准，绘图亦是如此
只有不断的实践才能总结出规律（理论），并让理论服务于实践
综合院大屏展示尺寸、力引导布局算法的特征、黄金分割率以及人眼垂直水平视觉差，画布的尺寸最终定在了1000px * 691.883px

后面在此该尺寸的画布上不断尝试各类参数及拓扑算法的绘图实验，选择好看、有意义的记录之。
考虑AS在注册时候，香港、台湾均和大陆单独分开的
因此提高到香港、台湾时，均指中国香港，中国台湾，而中国则是指中国大陆地区

# 实验1 国家（地区）Group互联关系组团(20200610)
Group: ["中国（大陆）", "日本", "俄罗斯", "中国（香港）"]
gravity=1,
repulsion=5,
画出的图，还可以，比之前散开的图要好看些，大体能充满画布，没有那么空
在进行该实验的过程中解决了程序自动生成高清图的问题，并实现了自动化绘制多年的对比星云图，可从时间维度上进行对比

解决了pyecharts资源本地引用的问题
通过自定义主题解决了不同类别的节点颜色自定义问题

中日韩 repulsion=20
中东盟 repulsion=15
中国（大陆+港澳台）repulsion=30
中德（2440Nodes, 4521Links） repulsion=15
中美（17718Nodes, 40476Links） repulsion=5 【用小黑跑直接Time Out，需要GPU加速啊】
中英（2647Nodes, 4745Links） repulsion=15
中法（1628Nodes, 3799Links） repulsion=20

# 实验2 舍去连线，绘制类The Internet Map的图（依然采用国家（地区）Group组团的形式）（20200610）
不需要再新建文件，直接编写新的绘制函数即可
经实验研究，echarts现有的力引导算法并不是很好的适用绘制The Internet Map图，需要根据自有力引导算法进行相应的改进
因此可以三个可能的优化方向中第三点结合起来，利用自有改进的力引导算法，计算并输出静态坐标。
再利用echarts的可视化能力，进行JS效果的网络图展示

# 实验3 研究机器学习聚类算法，从中寻找灵感
聚类算法是机器学习中涉及对数据进行分组的一种算法，在给定的数据集中，我们可以通过聚类算法将其分成一些不同的组。
在理论上，相同组的数据之间有相同的属性或者特征，不同组数据之间的属性或者特征相差比较大
聚类算法是一种非监督学习算法，并且作为常用的数据分析算法在很多领域上得到应用

K-Means
Mean-Shift
DBSCAN（基于密度的带噪声的空间聚类的应用）
基于高斯混合模型（GMM）的期望最大化（EM）聚类
凝聚层次聚类
图团体检测（Graph Community Detection）

"""
import json
import numpy as np
import csv

from pyecharts import options as opts
from pyecharts.charts import Graph
from pyecharts.globals import CurrentConfig
from pyecharts.datasets import register_files
import time

from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot

# 引用本地静态资源
CurrentConfig.ONLINE_HOST = "http://127.0.0.1:8000/"
# 使用自己构建的主题
register_files({"wayne": ["themes/wayne", "js"]})


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
    country_info_dict = {}
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        country_info_dict[line[4]] = line[5]
    return country_info_dict


def read_as_info(file_name, en2cn_country):
    """
    根据传入的as_core_map_data信息，读取as_info
    :param file_name:
    :param en2cn_country:
    :return as_info:
    :return cn_as:
    """
    as_info = []
    temp_dict = {}
    temp_dict_normal = {}
    temp_dict_label = {}
    file_read = open(file_name, 'r', encoding='utf-8')
    as_list = []  # 记录所有展示的as列表
    country_group = ["中国（大陆）", "法国"]
    # country_group_color = dict()
    # country_group_color["中国（大陆）"] = "red"
    # country_group_color["日本"] = "green"
    # country_group_color["俄罗斯"] = "blue"
    # country_group_color["中国（香港）"] = "yellow"

    for line in file_read.readlines():
        line = line.strip().split('|')
        try:
            country_cn = en2cn_country[line[8]].strip("\"")
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
    out_json = list()
    out_json.append(as_info_dict)
    out_json.append(as_links_dict)
    out_json.append(categories_dict)
    final_json = json.dumps(out_json, indent=4)
    with open("..\\000LocalData\\BGPlay\\Global_BGP_lay.json", 'a') as f:
        f.write(final_json)

    title_name = title_name + "[Nodes:" + str(len(as_info_dict)) + " Links:" + str(len(as_links_dict)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="1000px",
                                      height="691.883px",
                                      page_title=title_name,
                                      theme="wayne",
                                      bg_color="#000"))
        .add(
            series_name="",
            nodes=as_info_dict,
            links=as_links_dict,
            categories=categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=1,
            repulsion=20,
            linestyle_opts=opts.LineStyleOpts(width=0.5, opacity=0.3, color='source', curve=0),
            label_opts=opts.LabelOpts(is_show=False, font_size=8),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=14),
                                        legend_icon='roundRect')
                   )
        )
    return c


def graph_as_lay_no_line(title_name, country_en2cn, time_str) -> Graph:
    """
    尝试着不会绘制连线
    :param title_name:
    :param country_en2cn:
    :param time_str:
    :return:
    """
    file_in = '..\\000LocalData\\as_map\\as_core_map_data_new' + time_str + '1001.csv'
    bgp_file = "..\\000LocalData\\as_relationships\\serial-1\\" + time_str + "1001.as-rel.txt"
    as_info_dict, as_list, categories_dict = read_as_info(file_in, country_en2cn)
    print("Nodes:", len(as_info_dict))
    print("Categories:", len(categories_dict))
    print("As List:", len(as_list))
    as_links_dict = read_as_links(bgp_file, as_list)
    print("links:", len(as_links_dict))
    out_json = list()
    out_json.append(as_info_dict)
    out_json.append(as_links_dict)
    out_json.append(categories_dict)
    final_json = json.dumps(out_json, indent=4)
    with open("..\\000LocalData\\BGPlay\\Global_BGP_lay.json", 'a') as f:
        f.write(final_json)

    title_name = title_name + "[Nodes:" + str(len(as_info_dict)) + " Links:" + str(len(as_links_dict)) + "]"
    c = (
        Graph(init_opts=opts.InitOpts(width="1000px",
                                      height="691.883px",
                                      page_title=title_name,
                                      theme="wayne",
                                      bg_color="#000"))
        .add(
            series_name="",
            nodes=as_info_dict,
            links=as_links_dict,
            categories=categories_dict,
            # layout="circular",
            is_rotate_label=True,
            gravity=1,
            repulsion=5,
            linestyle_opts=opts.LineStyleOpts(width=0, opacity=0.3, color='source', curve=0),
            label_opts=opts.LabelOpts(is_show=False, font_size=8),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(font_size=14),
                                        legend_icon='roundRect')
                   )
        )
    return c


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    my_time_str = ["1999", "2004", "2009", "2014", "2019"]
    my_country_en2cn = gain_country_info()
    opt_title_name = "Graph-全球AS网络互联关系拓扑图"
    for str_item in my_time_str[-1:]:
        render_str = "..\\000LocalData\\BGPlay\\Global_BGP_lay" + str_item + ".html"
        img_str = "..\\000LocalData\\BGPlay\\Global_BGP_lay" + str_item + ".jpeg"
        make_snapshot(snapshot,
                      graph_as_lay(opt_title_name, my_country_en2cn, str_item).render(render_str),
                      img_str,
                      delay=30, pixel_ratio=12)

        print(img_str)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
