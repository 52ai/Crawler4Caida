# coding:utf-8
"""
create on Oct 24, 2019 by Wayne Yu
Function: 对全球BGP数据进行分析

1） 读取全球BGP关系数据，分析其互联方式的占比（peer or transit）
"""

import os
import matplotlib.pyplot as plt
import numpy as np


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
    t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    for item in data_list:
        print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))

    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, peer_list, t, transit_list)
    axs[0].set_xlim(0, len(date_list))
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('Peer and Transit')
    axs[0].grid(True)

    # cxy, f = axs[1].cohere(peer_list, transit_list, 256, 100. / dt)
    # axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    # file_path = ["../000LocalData/as_relationships/20151201.as-rel2.txt",
    #              "../000LocalData/as_relationships/20160901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20170901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20180901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20190901.as-rel2.txt"]
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(analysis(path_item))
        # print(result_list)
        temp_str = path_item.split('\\')[-1]
        date_list.append(temp_str.split('.')[0])
    draw(date_list, result_list)

