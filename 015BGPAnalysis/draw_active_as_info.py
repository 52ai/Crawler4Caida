# coding:utf-8
"""
create on Nov 12,2019 by Wayne YU
Function:


对active as info数据进行绘图分析，柱形图、折线图等
"""
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
import csv


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
    date_str = date_str.split("_")[-1]
    # 读取文件内容
    file_read = open(open_file, 'r', encoding='utf-8')
    normal_distribution_dic = {}
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        """
        以edge_cnt为key，计数为value，构建字典
        """
        if line[1] in normal_distribution_dic:  # 如果字典中含有该edge_cnt键
            normal_distribution_dic[line[1]] += 1
        else:
            normal_distribution_dic[line[1]] = 1
    # print(normal_distribution_dic)
    # 将字典排序输出
    normal_distribution_list = []
    temp_list = []
    x_list = []
    y_list = []
    for i in sorted(normal_distribution_dic.keys(), key=lambda item:int(item)):
        # print(i, normal_distribution_dic[i])
        temp_list.append(i)
        temp_list.append(normal_distribution_dic[i])
        normal_distribution_list.append(temp_list)
        x_list.append(i)
        y_list.append(normal_distribution_dic[i])
        temp_list = []
    print(normal_distribution_list)
    draw(x_list, y_list, date_str)


def draw(x_list, y_list, date_str):
    """
    对传入的数据进行绘图
    :param x_list:
    :param y_list:
    :param date_str:
    :return:
    """
    fig, ax = plt.subplots(1, 1, figsize=(50.0, 10.0))
    plt.xticks(rotation=90)
    tick_spacing = 4
    title_string = "Global BGP Relationships Distribution Analysis Graph " + date_str
    ax.set_title(title_string)
    # ax.plot(x_list, y_list, 'bo')
    ax.bar(x_list, y_list)
    ax.set_xlabel('Relationships Nums')
    ax.set_ylabel('COUNT')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    save_fig_name = "distribution_draw_bar" + date_str + ".jpg"
    plt.savefig(save_fig_name, dpi=1000)
    plt.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录开始时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\data"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    for path_item in file_path:
        analysis(path_item)
    # analysis(file_path[0])
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")