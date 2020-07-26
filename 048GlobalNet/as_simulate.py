# coding:utf-8
"""
create on July 26, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:
互联网之所以能发展到今天这个规模，正是因为它的开放和自由（OPEN&FREE）
该程序仅从学术研究的角度来讨论，US和FiveEye网络对CN网络全球可达性的影响
CN网络选择三家主要网络作为实验对象

1）中国电信，4134（163网）、4809（CN2网）
2）中国联通，4837（169网）、9929（IP承载A网）
3）中国移动，58453(移动国际公司)

US网络选择为
Verizon，701、702、703
HE，6939
NTT-US，2914
TATA-US，6453
Comcast，7922
Cogent，174
Sprint，1239
Level3,3356、3549
AT&T，7018
Zayo，6461
CenturyLink，209
PCCW-GlOBAL，3491

FiveEye网络选择为
UK-Vodafone，1273、9500
UK-British Telecommunications，5400
AU-Telstra，4637
CA-ROGERS，812
CA-BELL，577
NZ-Spark，4647

程序主要思路
求三个可达性，r0(原始全球可达性)、r1（剔除US网络，全球可达性）、r2（剔除FiveEye网络，全球可达性）
数据输入为最新全球互联网AS拓扑数据

"""
import time
import csv
import networkx as nx
from networkx.algorithms.flow import shortest_augmenting_path


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def reach_analysis(cn_as, us_as, five_as):
    """
    根据传入的cn_as、us_as、five_as，分别CN网络全球可达性指标r0、r1、r2
    先从简单的实现开始，后面再考虑算法的时间复杂度和空间复杂度
    :param cn_as:
    :param us_as:
    :param five_as:
    :return:
    """
    global_as_graph = nx.Graph()  # 生成空图，用于在内存中构建全球互联网网络拓扑
    print("CN AS Group:", cn_as)
    print("US AS Group:", us_as)
    print("Five AS Group:", five_as)
    as_rel_file = "../000LocalData/as_relationships/serial-1/20200701.as-rel.txt"
    file_read = open(as_rel_file, 'r', encoding='utf-8')
    global_as = []  # 存储全球所有的AS号
    global_reach_as = []  # 存储全球所有可达的AS号
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as_0 = str(line.strip().split('|')[0])
        as_1 = str(line.strip().split('|')[1])
        # 根据边构建全球互联网网络拓扑图
        global_as_graph.add_edge(as_0, as_1)
        # print(as_0, as_1)
        global_as.append(as_0)
        global_as.append(as_1)
        # 判断与CN网络直联的网络数量
        if as_0 in cn_as:
            global_reach_as.append(as_1)
        if as_1 in cn_as:
            global_reach_as.append(as_0)

    print("Global AS Count:", len(set(global_as)))
    print("Global Reach AS Count（直联情况）:", len(set(global_reach_as)))

    print("=>根据构建的全球AS拓扑图，统计全球网络拓扑特征")
    print("=>全球互联网网络拓扑图（原始）")
    print("拓扑图节点数量:", global_as_graph.number_of_nodes())
    print("拓扑图连边数量:", global_as_graph.number_of_edges())
    # print("图的平均连接性:", nx.all_pairs_node_connectivity(global_as_graph))
    # print("计算源目之间不相交的节点路径:", nx.node_disjoint_paths(global_as_graph, "4134", "4809"))
    # for item in list(nx.node_disjoint_paths(global_as_graph, "4134", "4809")):
    #     print(item)
    not_reach_as = []  # 存储不可达的网络
    reach_as = []  # 存储可达网络的数量
    for as_item in global_as_graph.nodes():
        reach_flag = 0  # 网络可达标记，默认为不可达
        for cn_as_item in cn_as:
            if nx.has_path(global_as_graph, cn_as_item, as_item):
                reach_flag = 1
                break
        if reach_flag == 1:
            reach_as.append(as_item)
        else:
            not_reach_as.append(as_item)
    print("CN网络到全球可达AS的数量：", len(reach_as))
    print("CN网络到全球不可达AS的数量：", len(not_reach_as))
    print("CN网络到全球可达性(r0):", len(reach_as)/len(set(global_as)))

    print("=>全球互联网网络拓扑图（剔除US-AS-Group）")
    for as_item in us_as:
        global_as_graph.remove_node(as_item)

    print("拓扑图节点数量:", global_as_graph.number_of_nodes())
    print("拓扑图连边数量:", global_as_graph.number_of_edges())
    not_reach_as = []  # 存储不可达的网络
    reach_as = []  # 存储可达网络的数量
    for as_item in global_as_graph.nodes():
        reach_flag = 0  # 网络可达标记，默认为不可达
        for cn_as_item in cn_as:
            if nx.has_path(global_as_graph, cn_as_item, as_item):
                reach_flag = 1
                break
        if reach_flag == 1:
            reach_as.append(as_item)
        else:
            not_reach_as.append(as_item)
    print("CN网络到全球可达AS的数量：", len(reach_as))
    print("CN网络到全球不可达AS的数量：", len(not_reach_as))
    print("CN网络到全球可达性(r1):", len(reach_as)/len(set(global_as)))

    print("=>全球互联网网络拓扑图（剔除FiveEye-AS-Group）")
    for as_item in five_as:
        global_as_graph.remove_node(as_item)

    print("拓扑图节点数量:", global_as_graph.number_of_nodes())
    print("拓扑图连边数量:", global_as_graph.number_of_edges())
    not_reach_as = []  # 存储不可达的网络
    reach_as = []  # 存储可达网络的数量
    for as_item in global_as_graph.nodes():
        reach_flag = 0  # 网络可达标记，默认为不可达
        for cn_as_item in cn_as:
            if nx.has_path(global_as_graph, cn_as_item, as_item):
                reach_flag = 1
                break
        if reach_flag == 1:
            reach_as.append(as_item)
        else:
            not_reach_as.append(as_item)
    print("CN网络到全球可达AS的数量：", len(reach_as))
    print("CN网络到全球不可达AS的数量：", len(not_reach_as))
    print("CN网络到全球可达性(r2):", len(reach_as)/len(set(global_as)))


if __name__ == "__main__":
    cn_as_group = ["4134", "4809", "4837", "9929", "58453"]
    us_as_group = ["701", "702", "703", "6939", "2914",
                   "6453", "7922", "174", "1239", "3356",
                   "3549", "7018", "6461", "209", "3491"]
    five_as_group_except_US = ["1273", "9500", "5400", "4637", "812",
                               "577", "4647"]
    time_start = time.time()  # 记录启动的时间
    reach_analysis(cn_as_group, us_as_group, five_as_group_except_US)
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
