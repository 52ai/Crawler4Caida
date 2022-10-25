# coding:utf-8
"""
create on May 1, 2020 by Wayne Yu
Function: 对全球BGP数据进行分析

读取全球BGP关系数据，分析其互联方式的占比（peer or transit）

Edition:

为了地图基础课题第一篇论文输出，重新绘图，使得排版更加美观
绘制的时间修改为19980101-20191201

v2: 20221025

服务于ThirdSCI论文的撰写，绘制时间19980101-20221001


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
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
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
    # print(data_list)
    # 存储绘图数据
    save_path_data_list = "../000LocalData/Paper_Data_Third/02_draw_rel.csv"
    write_to_csv(data_list, save_path_data_list)

    # dt = 1
    # t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    for item in data_list:
        # print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))

    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=32)
    plt.tick_params(labelsize=32)
    # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    font = {'family': 'Times New Roman',
            'style': 'normal',
            'weight': 'normal',
            'color': 'black',
            'size': 42
            }
    font_legend = {'family': 'Times New Roman',
                   'style': 'normal',
                   'weight': 'normal',
                   'size': 36
                   }
    tick_spacing = 12
    # ax.set_title("全球互联网BGP互联趋势分析(19980101-20191201)", font)
    ax.plot(draw_date, edge_list, ls='-', marker='.', label='All interconnected relationships')
    ax.plot(draw_date, peer_list, ls=':', marker='+', label='Peer relationship')
    ax.plot(draw_date, transit_list, ls='-.', marker='s', label='Transit relationship')
    ax.set_xlabel('Time of estimation', font)
    ax.set_ylabel('Interconnected relationship', font)
    ax.legend(prop=font_legend)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    save_path_fig = "..\\000LocalData\\Paper_Data_Third\\02_draw_rel_en.svg"
    plt.savefig(save_path_fig, dpi=600)
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    result_list = []
    date_list = []
    for path_item in file_path:
        result_list.append(analysis(path_item))
        temp_str = str(path_item.split('\\')[-1])
        date_list.append(temp_str.split('.')[0])
    # print(result_list)

    draw(date_list, result_list)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
