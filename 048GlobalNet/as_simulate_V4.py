# coding:utf-8
"""
create on July 28, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

V2:

在第一版的基础上，新增U和Five的AS号，第一版的数据中重要ISP的AS网络找的不全
这一版把重要ISP所有的注册AS网都剔除（可能存在一些，现网没有通告的AS号，在做剔除的时候，需要先做一个判断）

V3：
在第二版的基础上，新增对不可达AS的信息统计，如IP量（v4地址量）以及IP量所对应的区域
由于之前在caict_display的项目做过一些统计，此处暂时就先用统计后的结果，以节约IP量统计的时间
000LocalData/caict_display/as2ip_quantity_plus.csv
000LocalData/caict_display/as_info_format.csv

V4:
由于手动找会有遗漏，已因此在第三版的基础上，新增U+Five国家中的TOP ISP AS号，每个国家取其前10%的关键点（按照Transit  as Provider来统计）

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


def extract_as_info():
    """
    根据asn_info文件，提取as info 信息
    :return:
    """
    as2country_cn = gain_country_info()
    # file_in = "../000LocalData/as_map/as_core_map_data_new20200701.csv"
    # file_in_read = open(file_in, 'r', encoding='utf-8')
    # as2country_dict = {}  # 存储as号和国家对应关系的字典
    # for line in file_in_read.readlines():
    #     line = line.strip().split("|")
    #     # print(as2country_cn[line[1].split(",")[-1].strip()])
    #     as2country_dict[line[0]] = as2country_cn[line[8]].strip("\"")
    file_in = "../000LocalData/as_Gao/asn_info.txt"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    as2country_dict = {}  # 存储as号和国家对应关系的字典
    for line in file_in_read.readlines():
        line = line.strip().split("\t")
        # print(as2country_cn[line[1].split(",")[-1].strip()])
        as2country_dict[line[0]] = as2country_cn[line[1].split(",")[-1].strip()].strip("\"")
    return as2country_dict


def gain_as_ip_num(as_list):
    """
    根据传入的as_list，以as2ip_quantity_plus.csv作为输入，统计总的ip量
    :param as_list:
    :return global_ip_num:
    :return global_ip_prefix:
    :return has_ip_info_cnt:
    :return has_country_info)_cnt:
    """
    as2country_dict = extract_as_info()  # 存储as2country的中文信息
    # print("IP量统计AS计数:", len(as_list))
    global_ip_num, global_ip_prefix = 0, 0
    as2ip_num_dict = {}
    as2ip_num_file = "../000LocalData/caict_display/as2ip_quantity_plus.csv"
    file_read = open(as2ip_num_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        as2ip_num_dict[line[0].strip("AS")] = [line[1], line[2], line[3], line[4]]
    has_ip_info_cnt = 0  # 存储存在IP通告信息统计
    has_country_info_cnt = 0  # 存储存在国家信息统计
    rank_country_ip_num_dict = {}  # 存储每个国家通道IP量的统计
    for item_as in as_list:
        if item_as in as2ip_num_dict.keys():
            global_ip_num += int(as2ip_num_dict[item_as][1])
            global_ip_prefix += int(as2ip_num_dict[item_as][0])
            has_ip_info_cnt += 1
            if item_as in as2country_dict.keys():
                # print(as2country_dict[item_as])
                if as2country_dict[item_as] in rank_country_ip_num_dict.keys():
                    rank_country_ip_num_dict[as2country_dict[item_as]] += int(as2ip_num_dict[item_as][1])
                else:
                    rank_country_ip_num_dict[as2country_dict[item_as]] = int(as2ip_num_dict[item_as][1])
                has_country_info_cnt += 1
    # print(rank_country_ip_num_dict)
    return global_ip_num, global_ip_prefix, has_ip_info_cnt, has_country_info_cnt, rank_country_ip_num_dict


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
    # print("US AS Group:", us_as)
    # print("Five AS Group:", five_as)
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
    global_ip_num, global_ip_prefix, has_ip_info_cnt, has_country_info_cnt, country_ip_dict = gain_as_ip_num(reach_as)
    cn_ip_num = country_ip_dict["中国（大陆）"]
    print("地址统计has_info(IP)校验：", has_ip_info_cnt)
    print("地址统计has_info(Country)校验：", has_country_info_cnt)
    print("CN网络到全球可达前缀数量:", global_ip_prefix)
    print("CN网络到全球可达IP地址数量规模:", (global_ip_num-cn_ip_num))
    original_global_ip_prefix = global_ip_prefix
    original_global_ip_num = global_ip_num - cn_ip_num  # 中国到全球，应该把中国地址刨去
    print("CN网络到全球前缀可达性(r0):", global_ip_prefix/original_global_ip_prefix)
    print("CN网络到全球IPv4地址可达性(r0):", (global_ip_num-cn_ip_num)/original_global_ip_num)

    print("\n=>全球互联网网络拓扑图（剔除U-AS-Group）")
    print("输入剔除的网络个数:", len(us_as))
    remove_cnt = 0  # 记录剔除的网络个数
    for as_item in us_as:
        if as_item in global_as_graph.nodes():
            global_as_graph.remove_node(as_item)
            remove_cnt += 1
    print("实际剔除的网络个数:", remove_cnt)
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
    global_ip_num, global_ip_prefix, has_ip_info_cnt, has_country_info_cnt, country_ip_dict = gain_as_ip_num(reach_as)
    print("地址统计has_info(IP)校验：", has_ip_info_cnt)
    print("地址统计has_info(Country)校验：", has_country_info_cnt)
    # print("CN网络到全球可达前缀数量:", global_ip_prefix)
    print("CN网络到全球可达IP地址数量规模:", (global_ip_num-cn_ip_num))
    # print("CN网络到全球前缀可达性(r1):", global_ip_prefix/original_global_ip_prefix)
    print("CN网络到全球IPv4地址可达性(r1):", (global_ip_num-cn_ip_num)/original_global_ip_num)

    print("\n=>全球互联网网络拓扑图（剔除Five-AS-Group）")
    for as_item in five_as:
        if as_item in global_as_graph.nodes():
            global_as_graph.remove_node(as_item)
            remove_cnt += 1
    print("输入剔除的网络个数:", (len(us_as)+len(five_as)))
    print("累计剔除的网络个数:", remove_cnt)
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
    global_ip_num, global_ip_prefix, has_ip_info_cnt, has_country_info_cnt, country_ip_dict = gain_as_ip_num(reach_as)
    print("地址统计has_info(IP)校验：", has_ip_info_cnt)
    print("地址统计has_info(Country)校验：", has_country_info_cnt)
    # print("CN网络到全球可达前缀数量:", global_ip_prefix)
    print("CN网络到全球可达IP地址数量规模:", (global_ip_num-cn_ip_num))
    # print("CN网络到全球前缀可达性(r2):", global_ip_prefix/original_global_ip_prefix)
    print("CN网络到全球IPv4地址可达性(r2):", (global_ip_num-cn_ip_num)/original_global_ip_num)


def gain_u_five_as_group():
    """
    根据as core map file 获取U+file TOP ISP AS号
    :return:
    """
    u_as_group = []
    five_as_group = []
    file_in = "../000LocalData/as_map/as_core_map_data_new20200701.csv"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    for line in file_in_read.readlines():
        line = line.strip().split("|")
        if line[8] == "DC":
            u_as_group.append(line)
        if line[8] in ["UK", "AU", "CA", "NZ"]:
            five_as_group.append(line)
    print("u_as_group len:", len(u_as_group))
    print("five_as_group len:", len(five_as_group))
    u_as_group.sort(reverse=True, key=lambda elem: int(elem[3]))
    u_as_group_re = []  # 存储返回的TOP ISP AS列表
    for item in u_as_group[0:1000]:
        u_as_group_re.append(item[0])
        print(item)

    five_as_group.sort(reverse=True, key=lambda elem: int(elem[3]))
    five_as_group_re = []  # 存储返回的TOP ISP AS列表
    for item in five_as_group[0:2000]:
        five_as_group_re.append(item[0])
        print(item)
    return u_as_group_re, five_as_group_re


if __name__ == "__main__":
    cn_as_group = ["4134", "4809", "4837", "9929", "58453"]
    my_u_as_group, my_five_as_group = gain_u_five_as_group()
    time_start = time.time()  # 记录启动的时间
    reach_analysis(cn_as_group, my_u_as_group, my_five_as_group)
    time_end = time.time()  # 记录结束的时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
