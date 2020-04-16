# coding:utf-8
"""
create on Apr 1, 2020 By Wenyan YU
Function:

基于OPNET的全球 TOPN ISP网络互联仿真模型（小型）

大致思路，基于OPNET SPGuru 构建AS级互联模型，包括逻辑层上的AS级拓扑图以及每个AS基于地理位置的域内拓扑图。
需要做的数据整理工作如下：

1）从全球6万多个AS网络中，选取TOP 100的ISP自治域网络；从全国500多个AS网络中，选取TOP 5的ISP自治域网络。（100+5）
2）针对每个自治域网络号码进行全球POP点位置数据采集、路由通告前缀信息采集、互联AS及其商业关系、互联地理位置采集。

目前手里头已有数据：

20200201.as-rel.txt 全球互联网AS级互联关系数据
as_core_map_data_new20200201.csv 地图课题时整理的全球AS网络画像
asnip.txt ASN号对应的所属IP地址
201603.as-rel-geo.txt AS间互联的地理位置（后面没有更新了，数据不全）

"""

import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定的路径文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s>..." % des_path)
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


def gain_resource_data():
    """
    根据已掌握的数据，处理得到OPNET模型输入数据
    :return:
    """
    as_portrait_file = "..\\000LocalData\\OPNet\\as_core_map_data_new20200201.csv"
    asn2ip_file = "..\\000LocalData\\OPNet\\asnip.txt"
    as_rel_geo_file = "201603.as-rel-geo.txt"

    # 读入AS网络画像文件信息，提取Global TOP 100和CN TOP 5的ISP网络
    as_portrait_list = []  # 存储AS网络画像List
    as_portrait_cn_list = []  # 存储中国活跃的AS网络画像List
    as_portrait_file_read = open(as_portrait_file, 'r', encoding='utf-8')
    for line in as_portrait_file_read.readlines():
        line = line.strip().split("|")
        as_portrait_list.append(line)
        if line[8] == "CN":
            # 获取中国活跃的AS号
            as_portrait_cn_list.append(line)
        # print(line)
    print("全球活跃AS总数：", len(as_portrait_list))
    print("中国活跃AS总数：", len(as_portrait_cn_list))
    # 以Transit as Provider的统计值作为排序基准，对全球活跃AS号集合进行排序
    as_portrait_list.sort(reverse=True, key=lambda elem: int(elem[3]))
    # 存储as_portrait_Global(ISP rank)
    save_path = "..\\000LocalData\\OPNet\\as_portrait_Global(ISP rank).csv"
    write_to_csv(as_portrait_list, save_path)
    as_portrait_cn_list.sort(reverse=True, key=lambda elem: int(elem[3]))
    # 存储as_portrait_CN(ISP rank)
    save_path = "..\\000LocalData\\OPNet\\as_portrait_CN(ISP rank).csv"
    write_to_csv(as_portrait_cn_list, save_path)
    # 根据排序后的集合，获取Global TOP 100 AS和CN TOP 5 AS
    top_as_global = [line[0] for line in as_portrait_list[:30]]
    print(top_as_global)
    top_as_cn = [line[0] for line in as_portrait_cn_list[:5]]
    print(top_as_cn)
    top_as = list(set(set(top_as_global) | set(top_as_cn)))
    # print(len(top_as))
    # print(top_as)
    draw_as_rel(top_as)


def draw_as_rel(as_list):
    """
    根据传入的as List信息，结合全球互联网AS级互联关系数据，绘制该AS集合中的互联关系
    :param as_list:
    :return:
    """
    rel_file = "..\\000LocalData\\OPNet\\20200201.as-rel.txt"
    top_as = as_list
    print("TOP AS（ISP）总数:", len(top_as))
    top_as_rel = []  # 存储TOP AS 之间的互联关系
    rel_file_read = open(rel_file, "r", encoding='utf-8')
    for line in rel_file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        if line[0] in top_as and line[1] in top_as:
            # print(line)
            top_as_rel.append(line)
    print("TOP AS Relationships 总数:", len(top_as_rel))
    # 存储top_as_rel(ISP).csv
    save_path = "..\\000LocalData\\OPNet\\as_relationships(TOP ISP).csv"
    write_to_csv(top_as_rel, save_path)
    # 存储as_list(TOP ISP).csv
    save_path = "..\\000LocalData\\OPNet\\as_list(TOP ISP).csv"
    write_to_csv([top_as], save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    gain_resource_data()
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")