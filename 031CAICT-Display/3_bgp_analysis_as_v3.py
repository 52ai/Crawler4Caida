# coding:utf-8
"""
create on Mar 11, 2020 by Wayne Yu
Email: ieeflsyu@outlook.com

Function: 对全球BGP数据进行分析，并针对某一个AS的历史BGP互联信息进行分析

全球TOP20和全国TOP20

"""

import os
import csv
import time


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


def analysis(open_file, as_analysis):
    """
    对数据进行分析处理
    :param open_file:
    :param as_analysis:
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
        if line.strip().split('|')[0] == as_analysis:  # 如果位于第一位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_provider_cnt += 1
            edge_cnt += 1

        if line.strip().split('|')[1] == as_analysis:  # 如果位于第二位
            if line.strip().split('|')[2] == '0':
                peer_cnt += 1
            if line.strip().split('|')[2] == '-1':
                transit_customer_cnt += 1
            edge_cnt += 1
        # if edge_cnt > 1000:
        #     break

    return edge_cnt, peer_cnt, transit_provider_cnt + transit_customer_cnt,transit_provider_cnt, transit_customer_cnt


def draw(draw_date, data_list, as_analysis):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    # 将绘图的信息存储U起来
    save_list = []
    temp_list = []
    for i in range(0, len(draw_date)):
        temp_list.append(draw_date[i])
        temp_list.extend(data_list[i])
        save_list.append(temp_list)
        # print(temp_list)
        temp_list = []
    # date、All、peer、Transit、transit as provider、transit as customer
    save_path = "../000LocalData/caict_display/draw_AS" + as_analysis + ".csv"
    write_to_csv(save_list, save_path)


if __name__ == "__main__":
    time_start = time.time()
    as_analysis = []
    topas20global_file = "../000LocalData/caict_display/topas20Global_2019.csv"
    topas20CN_file = "../000LocalData/caict_display/topas20CN_2019.csv"
    topas20global_in = open(topas20global_file, 'r', encoding='utf-8')
    topas20CN_in = open(topas20CN_file, 'r', encoding='utf-8')
    # 获取全球TOP20AS号
    for line in topas20global_in.readlines():
        line = line.strip().split("|")
        as_analysis.append(line[0])
    # 获取全国TOP20AS号
    for line in topas20CN_in.readlines():
        line = line.strip().split("|")
        as_analysis.append(line[0])
    print(as_analysis)
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    result_list = []
    date_list = []
    for as_item in as_analysis:
        for path_item in file_path:
            result_list.append(analysis(path_item, as_item))
            # print(result_list)
            temp_str = path_item.split('\\')[-1]
            date_list.append(temp_str.split('.')[0])
        draw(date_list, result_list, as_item)
        result_list = []  # 清空result_list
        date_list = []  # 清空date_list
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
