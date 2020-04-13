# coding:utf-8
"""
create on Jan 20, 2020 By Wayne YU

Function:

该程序用统计以国家为单位的活跃AS号数量，并通过pyecharts绘图

"""

import time
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


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
    return date_str, active_as_global, active_as_country


def draw(draw_data, country_str):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    draw_date = []
    global_list = []
    country_list = []
    for item in draw_data:
        # print(int(item[0]))
        draw_date.append(item[0])
        global_list.append(int(item[1]))
        country_list.append(int(item[2]))

    fig, ax = plt.subplots(1, 1, figsize=(30, 15))
    plt.xticks(rotation=30)
    tick_spacing = 6
    title_string = country_str + " Active As Graph(19980101-20200201)"
    ax.set_title(title_string)
    # ax.plot(draw_date, global_list, linewidth=2, linestyle=':', label='Global Active AS', marker='o')
    ax.plot(draw_date, country_list, linewidth=1, linestyle='--', label='China Active AS', marker='+')
    # ax.set_xlim(0, len(date_list))
    ax.set_xlabel('Time')
    ax.set_ylabel('Active AS Nums')
    ax.legend()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # ax.grid(True)
    # cxy, f = axs[1].cohere(peer_list, transit_list, 256, 100. / dt)
    # axs[1].set_ylabel('coherence')
    # fig.tight_layout()
    plt.savefig("..\\000LocalData\\RUNet\\active_as_bar_" + country_str + ".jpg")
    # plt.show()


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country_str = "RU"
    # 获取历年活跃AS数量列表
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_map"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    active_as_ru = []
    temp_list = []
    for path_item in file_path:
        dateStr, activeAS_country, activeAS_global = gain_active_as(path_item, country_str)
        temp_list.append(dateStr)
        temp_list.append(activeAS_country)
        temp_list.append(activeAS_global)
        active_as_ru.append(temp_list)
        print(temp_list)
        temp_list = []
    draw(active_as_ru, country_str)
    # save_path
    save_path = "..\\000LocalData\\RUNet\\active_as_" + str.lower(country_str) + ".csv"
    write_to_csv(active_as_ru, save_path)
    time_end = time.time()
    print("\n=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
