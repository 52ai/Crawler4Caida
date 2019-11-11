# coding:utf-8
"""
create on Nov 11, 2019 by Wayne Yu
Function: 对全球BGP数据进行分析

读取全球BGP关系数据，分析其互联方式的占比（peer or transit）
All、Peer、Transit分开画图
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
    对数据进行分析处理
    :param open_file:
    :return:
    """
    file_read = open(open_file, 'r', encoding='utf-8')
    edge_cnt = 0
    peer_cnt = 0
    transit_cnt = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip().split('|'))
        if line.strip().split('|')[2] == '0':
            peer_cnt += 1
        if line.strip().split('|')[2] == '-1':
            transit_cnt += 1
        edge_cnt += 1
        # if edge_cnt > 1000:
        #     break

    return edge_cnt, peer_cnt, transit_cnt


def draw(draw_date, data_list):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    edge_list = []
    peer_list = []
    transit_list = []
    for item in data_list:
        print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))

    draw_list("All_Relationships", draw_date, edge_list)
    draw_list("Peer", draw_date, peer_list)
    draw_list("Transit", draw_date, transit_list)


def draw_list(pic_name, date_list, draw_list):
    """
    对传入的list进行绘图
    :param pic_name:
    :param draw_list:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=30)
    tick_spacing = 6
    title_string = "Global BGP Analysis Graph(19980101-20191001)-" + pic_name
    ax.set_title(title_string)
    ax.plot(date_list, draw_list)
    ax.set_xlabel('Time')
    ax.set_ylabel('Relationships Nums')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    save_fig_name = "draw_rel1_"+pic_name+".jpg"
    plt.savefig(save_fig_name, dpi=1000)


if __name__ == "__main__":
    # file_path = ["../000LocalData/as_relationships/20151201.as-rel2.txt",
    #              "../000LocalData/as_relationships/20160901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20170901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20180901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20190901.as-rel2.txt"]
    time_start = time.time()
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(analysis(path_item))
        print(result_list)
        temp_str = path_item.split('\\')[-1]
        date_list.append(temp_str.split('.')[0])
    bgp_analysis_save = "./data/bgp_analysis_result_21years.csv"
    bgp_analysis_result = []
    temp_save = []
    for i in range(0, len(date_list)):
        temp_save.append(date_list[i])
        temp_save.extend(result_list[i])
        bgp_analysis_result.append(temp_save)
        temp_save = []
    write_to_csv(bgp_analysis_result, bgp_analysis_save)

    draw(date_list, result_list)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")

