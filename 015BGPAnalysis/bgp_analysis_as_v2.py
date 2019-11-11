# coding:utf-8
"""
create on Nov 11, 2019 by Wayne Yu
Function: 对全球BGP数据进行分析，并针对某一个AS的历史BGP互联信息进行分析

1）CDN企业
Akamai, 32787

2)云服务商
google, 15169
阿里云，45102
腾讯云，132203

03)ISP
AT&T Services,Inc, 7018
Verizon，701
NTT, 2914
电信，4134
联通，4837

暴风电子,6939
Level 3, 3549
Cogent, 174
西班牙电信，12956
Comcast, 7922

"""

import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import time


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
    dt = 1
    # t = np.arange(0, len(draw_date), dt)
    edge_list = []
    peer_list = []
    transit_list = []
    transit_provider_list = []
    transit_customer_list = []
    for item in data_list:
        print(int(item[0]))
        edge_list.append(int(item[0]))
        peer_list.append(int(item[1]))
        transit_list.append(int(item[2]))
        transit_provider_list.append(int(item[3]))
        transit_customer_list.append(int(item[4]))

    fig, ax = plt.subplots(1, 1, figsize=(19.2, 10.8))
    plt.xticks(rotation=30)
    tick_spacing = 6
    title_string = "Global BGP Analysis Graph(19980101-20191001) AS:" + as_analysis
    ax.set_title(title_string)
    ax.plot(draw_date, edge_list, label='All AS-Relationships')
    ax.plot(draw_date, peer_list, label='Peer')
    ax.plot(draw_date, transit_list, label='Transit')
    # ax.plot(draw_date, transit_provider_list, label='Transit(as Provider)')
    # ax.plot(draw_date, transit_customer_list, label='Transit(as Customer)')
    # ax.set_xlim(0, len(date_list))
    ax.set_xlabel('Time')
    ax.set_ylabel('Relationships Nums')
    ax.legend()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # ax.grid(True)
    # cxy, f = axs[1].cohere(peer_list, transit_list, 256, 100. / dt)
    # axs[1].set_ylabel('coherence')
    # fig.tight_layout()
    plt.savefig("draw_AS"+ as_analysis+".jpg")
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()
    as_analysis = ["32787", "13335", "54994", "63541",
                   "16509", "8075", "15169", "37963", "45102", "45090", "132203", "38365", "55967",
                   "4134", "4837", "7018", "701", "2914", "6939", "3549", "174", "12956", "7922"]
    # file_path = ["../000LocalData/as_relationships/20151201.as-rel2.txt",
    #              "../000LocalData/as_relationships/20160901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20170901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20180901.as-rel2.txt",
    #              "../000LocalData/as_relationships/20190901.as-rel2.txt"]
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            # print(os.path.join(root, file_item))
            file_path.append(os.path.join(root, file_item))
    print(file_path)
    result_list = []
    date_list = []
    for as_item in as_analysis:
        for path_item in file_path:
            result_list.append(analysis(path_item, as_item))
            print(result_list)
            temp_str = path_item.split('\\')[-1]
            date_list.append(temp_str.split('.')[0])
        draw(date_list, result_list, as_item)
        result_list = []  # 清空result_list
        date_list = []  # 清空date_list
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
