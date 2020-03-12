# coding:utf-8

"""
create on Mar 4, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

针对院大屏系统所需的绘图数据，做统一的集成处理，实现一键出数据。

1）全球BGP互联关系变化趋势（时间+统计值，包括All Relationships、Peer、Transit =》完成
2）全球BGP互联关系数据量统计分布图（互联数量+统计值，无标度网络特征出现，后续再进一步研究）（直接绘制1998-2019）=》完成
3）全球各主要国家国内BGP互联关系变化趋势（时间+国内BGP互联关系数量）【另附文件】=》完成
4）全球各主要国家对外BGP互联关系变化趋势（时间+对外BGP互联关系数量）【另附文件】=》完成
5）代表性AS互联关系变化趋势（全球TOP AS 20、全国TOP AS 20，时间+BGP互联关系统计值5项）【另附文件】=》完成
6）我国出口AS互联关系统计（互联国家+互联关系总数）（直接绘制1998-2019）【另附文件】=》完成

"""
import os
import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csvFile = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csvFile, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def bgp_analysis_step(open_file):
    """
    对传入的数据文件进行统计All Rel、Peer、Transit
    :param open_file:
    :return:
    """
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt, peer_cnt, transit_cnt = 0, 0, 0
    for line in file_read.readlines():
        # 绕过文件头部注释
        if line.strip().find("#") == 0:
            continue
        if line.strip().split('|')[2] == '0':
            peer_cnt += 1
        if line.strip().split('|')[2] == '-1':
            transit_cnt += 1
        edge_cnt += 1
    return edge_cnt, peer_cnt, transit_cnt


def bgp_analysis():
    """
    统计全球BGP互联关系变化趋势，时间+统计值，包括All Relationships、Peer、Transit
    :return:
    """
    file_path = []
    # 获取文件夹下所有的文件
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(bgp_analysis_step(path_item))
        temp_str = path_item.split('\\')[-1]
        date_list.append(temp_str.split(".")[0])
    bgp_analysis_result = []
    temp_save = []
    for i in range(0, len(date_list)):
        temp_save.append(date_list[i])
        temp_save.extend(result_list[i])
        bgp_analysis_result.append(temp_save)
        temp_save = []
    bgp_analysis_save = "../000LocalData/caict_display/bgp_analysis_result_21years.csv"
    write_to_csv(bgp_analysis_result, bgp_analysis_save)  # 写CSV文件


def bgp_degree_gain_as_rel(asn, open_file):
    """
    根据传入的asn,统计其bgp互联关系（All, Peer, Transit），并返回
    :param asn:
    :param open_file:
    :return:
    """
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_provider_cnt = 0
    transit_customer_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[0] == asn:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

        if line.strip().split('|')[1] == asn:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1
    return edge_cnt, peer_cnt, transit_provider_cnt + transit_customer_cnt


def bgp_degree_distribution_step(open_file):
    """
    对传入的文件中AS号进行节点度分布的统计
    :param open_file:
    :return:
    """
    print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        """
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    print("Active AS：", len(as_list))

    """
    获取活跃AS列表之后，针对每一个AS号统计其互联关系数量，AS_Relationships、Peer、Transit
    """
    active_as_info = []  # 存储所有活跃的AS号的BGP互联信息
    temp_list = []
    for as_item in as_list:
        # print(as_item)
        edge_cnt, peer_cnt, transit_cnt = bgp_degree_gain_as_rel(as_item, open_file)
        temp_list.append(as_item)
        temp_list.append(edge_cnt)
        temp_list.append(peer_cnt)
        temp_list.append(transit_cnt)
        active_as_info.append(temp_list)
        # print(temp_list)
        temp_list = []
    # 将active_as_info存储为文件
    save_path = "../000LocalData/caict_display/active_as_info_" + date_str + ".csv"
    write_to_csv(active_as_info, save_path)


def bgp_degree_distribution():
    """
    统计某一时间AS度的分布
    :return:
    """
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-3"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    for path_item in file_path:
        bgp_degree_distribution_step(path_item)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # bgp_analysis()  # 1）统计全球BGP互联关系变化趋势
    bgp_degree_distribution()  # 2） 全球BGP互联关系数据量统计分布图
    time_end = time.time()  # 记录结束时间
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")




