# coding:utf-8
"""
create on Jan 20, 2020 By Wayne YU

Function:

该程序用统计以国家为单位的活跃AS号数量，并通过pyecharts绘图

"""

import time
import csv
import os


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
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_active_as(as_info, country_str):
    """
    根据传入的as info，返回active的数量
    :param as_info:
    :return active_as_cnt:
    """
    # 处理名称，提取日期信息
    temp_str = as_info.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    date_str = date_str[-8:]
    ru_as_info = []  # 存储ru as 信息
    file_read = open(as_info, 'r', encoding='utf-8')
    active_as_global = 0
    for line in file_read.readlines():
        line = line.strip().split("|")
        if line[8] == country_str:
            ru_as_info.append(line)
        active_as_global += 1
    active_as_country = len(ru_as_info)
    return date_str, active_as_country, active_as_global


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # 获取历年活跃AS数量列表
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_map"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    active_as_ru = []
    temp_list = []
    for path_item in file_path:
        dateStr, activeAS_country, activeAS_global = gain_active_as(path_item, "IN")
        temp_list.append(dateStr)
        temp_list.append(activeAS_country)
        temp_list.append(activeAS_global)
        active_as_ru.append(temp_list)
        print(temp_list)
        temp_list = []
    # save_path
    save_path = "..\\000LocalData\\RUNet\\active_as_in.csv"
    write_to_csv(active_as_ru, save_path)
    time_end = time.time()
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
