# coding:utf-8
"""
create on May 1, 2020 by Wayne Yu
Function: 对全球BGP数据进行分析

1） 读取全球BGP关系数据，分析其互联方式的占比（peer or transit）

Edition:

为了地图基础课题第一篇论文输出，重新绘图，使得排版更加美观
绘制的时间修改为19980101-20191201

"""

import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import time


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
    dt = 1
    # t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    for item in data_list:
        print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))

    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=30)
    plt.tick_params(labelsize=32)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    font = {'family': 'sans-serif',
            'style': 'normal',
            'weight': 'normal',
            'color': 'black',
            'size': 42
            }
    font_legend = {'family': 'sans-serif',
                   'style': 'normal',
                   'weight': 'normal',
                   'size': 36
                   }
    tick_spacing = 12
    # ax.set_title("全球互联网BGP互联趋势分析(19980101-20191201)", font)
    ax.plot(draw_date, edge_list, ls='-', marker='.', label='All Relationships')
    ax.plot(draw_date, peer_list, ls=':', marker='+', label='Peer')
    ax.plot(draw_date, transit_list, ls='-.', marker='s', label='Transit')
    ax.set_xlabel('Statistical Time(UTC)', font)
    ax.set_ylabel('Number of Relationships', font)
    ax.legend(prop=font_legend)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    plt.savefig("../000LocalData/Paper_Data/draw_rel1_en.jpg", dpi=720)
    # plt.show()


if __name__ == "__main__":
    # file_path = ["../000LocalData/as_relationships/20151201.as-rel2.txt",
    #              "../000LocalData/as_relationships/20160901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20170901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20180901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20190901.as-rel2.txt"]
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-4"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(analysis(path_item))
        temp_str = path_item.split('\\')[-1]
        date_list.append(temp_str.split('.')[0])
    print(result_list)

    draw(date_list, result_list)

