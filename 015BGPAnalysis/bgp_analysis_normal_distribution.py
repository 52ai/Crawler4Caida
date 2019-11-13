# coding: utf-8
"""
create on Nov 12, 2019 by Wayne Yu
Function:

通过分析全球BGP互联数据，来研究其分布方式（预计为正态分布）

"""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
        writer = csv.writer(csvFile)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def analysis(open_file):
    """
    对数据进行处理
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
        # if line.strip().split('|')[0] not in as_list:
        #     as_list.append(line.strip().split('|')[0])
        # if line.strip().split('|')[1] not in as_list:
        #     as_list.append(line.strip().split('|')[1])
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    # print(as_list)
    print("Active AS：", len(as_list))

    """
    获取活跃AS列表之后，针对每一个AS号统计其互联关系数量，AS_Relationships、Peer、Transit
    """
    active_as_info = []  # 存储所有活跃的AS号的BGP互联信息
    temp_list = []
    for as_item in as_list:
        # print(as_item)
        edge_cnt, peer_cnt, transit_cnt = gain_as_rel(as_item, open_file)
        temp_list.append(as_item)
        temp_list.append(edge_cnt)
        temp_list.append(peer_cnt)
        temp_list.append(transit_cnt)
        active_as_info.append(temp_list)
        # print(temp_list)
        temp_list = []
    # 将active_as_info存储为文件
    save_path = "../000LocalData/as_relationships/data/active_as_info_" + date_str + ".csv"
    write_to_csv(active_as_info, save_path)


def gain_as_rel(asn, open_file):
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


def draw(data_list):
    """
    对数据进行绘图
    :param data_list:
    :return:
    """
    pass


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-3"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    for path_item in file_path:
        analysis(path_item)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

"""
run-log:
C:\Python37\python.exe D:/Code/Crawler4Caida/015BGPAnalysis/bgp_analysis_normal_distribution.py
..\000LocalData\as_relationships\serial-3\19980101.as-rel.txt
Active AS： 3233
write file <../000LocalData/as_relationships/data/active_as_info_19980101.csv> ...
write finish!
..\000LocalData\as_relationships\serial-3\20041001.as-rel.txt
Active AS： 18454
write file <../000LocalData/as_relationships/data/active_as_info_20041001.csv> ...
write finish!
..\000LocalData\as_relationships\serial-3\20091001.as-rel.txt
Active AS： 32826
write file <../000LocalData/as_relationships/data/active_as_info_20091001.csv> ...
write finish!
..\000LocalData\as_relationships\serial-3\20141001.as-rel.txt
Active AS： 46120
write file <../000LocalData/as_relationships/data/active_as_info_20141001.csv> ...
write finish!
..\000LocalData\as_relationships\serial-3\20191001.as-rel.txt
Active AS： 66488
write file <../000LocalData/as_relationships/data/active_as_info_20191001.csv> ...
write finish!
=>Scripts Finish, Time Consuming: 44216.931780576706 S
"""