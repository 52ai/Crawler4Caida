# coding:utf-8
"""
create on Feb 6, 2020 By Wayne YU

Function:

俄罗斯断网事件分析后续
针对俄罗斯断网事件，分析了TOP 100的AS网络总连接数、国内连接总数、国外连接总数近2年的变化情况，并没有发现几个独大的AS
因此从单个AS互联关系数量的变化上看并不能发现什么

在这里要明确一些事情，俄罗斯断网事件是一个国家行为，需要把整个俄罗斯作为一个整体去考虑
从全局去看俄罗斯出口AS数量变化及其互联方向（国家）统计分析可能会有所发现

出口AS定义为与国外AS存在互联关系的AS号

该程序要实现的是输入一个国家，统计该国家的出口AS号数量及其出口互联方向（国家）统计分析

此外从BGP角度为进一步分析周边中亚国家到其他国家的路由是否通过俄罗斯中转
可对中亚六国哈萨克斯坦（KZ）、吉尔吉斯斯坦(KG)、塔吉克斯坦（TJ）、乌兹别克斯坦(UZ)、土库曼斯坦(TM)、阿富汗斯坦（AF）

哈萨克斯坦（Kazakhstan， KZ），各国方向都有（见绘图）
吉尔吉斯斯坦（Kyrgyzstan， KG），各国方向都有（见绘图）
塔吉克斯坦（Tajikistan， TJ），只有2个国外互联方向，俄罗斯（15条边），吉尔吉斯斯坦（1条边）
只与俄罗斯互联的塔吉克斯坦AS网络：['48001', '15881', '42713', '43197', '48184', '205507', '57443', '48887', '34557', '8847']


乌兹别克斯坦（Uzbekistan, UZ），各国方向都有，以乌克兰为主（见绘图）
土库曼斯坦（Turkmenistan， TM），只有3个国外互联方向，俄罗斯（2条边），哈萨克斯坦（1条边），美国（1条边）)
阿富汗斯坦（Afghanistan， AF），各国方向都有（见绘图）

"""

import time
import csv
import os
import matplotlib.pyplot as plt


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


def gain_as2country(as_info_file, country):
    """
    根据传入的as info file信息获取AS与国家的对应字典及该国家的所有的AS Info
    :param as_info_file:
    :param country:
    :return country_as_info:
    :return as2country:
    """
    country_as_info = []  # 存储country as 信息
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    # for line in file_read.readlines():
    #     line = line.strip().split("|")
    #     as2country[line[0]] = line[8]  # 生成字典
    #     temp_list = []
    #     if line[8] == country:
    #         temp_list.append(line[0])  # AS Number
    #         temp_list.append(line[1])  # AS All Relationships
    #         temp_list.append(line[5])  # AS Name
    #         temp_list.append(line[7])  # Source
    #         temp_list.append(line[8])  # Country
    #         country_as_info.append(temp_list)

    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_name = line[1].strip().split(",")[0].strip()
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
        temp_list = []
        if as_country == country:
            temp_list.append(as_number)
            temp_list.append(as_name)
            temp_list.append(as_country)
            country_as_info.append(temp_list)

    return country_as_info, as2country


def external_as_analysis(country, country_as_info, as2country):
    """
    根据输入的国家，统计该国家的出口AS数量及其互联方向的统计分析
    :param country:
    :param country_as_info:
    :param as2country:
    :return:
    """
    print(country)
    # 获取1998-2020年间全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    for path_item in file_path[-1:]:
        print(path_item)
        # 遍历一次文件，获取该国出口AS的数量
        file_read = open(path_item, 'r', encoding='utf-8')
        external_cnt = 0  # 存储该国出口连边的数量
        external_as_list = []  # 存储出口AS
        external_country_list = []  # 存储该国出口方向的国家
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if as2country[str(line.strip().split('|')[0])] == country:
                    if as2country[str(line.strip().split('|')[1])] != country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[0]))
                        external_country_list.append(as2country[str(line.strip().split('|')[1])])
                else:
                    if as2country[str(line.strip().split('|')[1])] == country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[1]))
                        external_country_list.append(as2country[str(line.strip().split('|')[0])])

            except Exception as e:
                pass
        external_as_list = list(set(external_as_list))
        print("External Edges Count:", external_cnt)
        print("External AS Count:", len(external_as_list))
        # print(external_as_list)
        # 统计小于65535的AS号
        # v4_as_list = []
        # for as_item in external_as_list:
        #     if int(as_item) < 65535:
        #         v4_as_list.append(as_item)
        # # print(v4_as_list)
        # print("V4 AS Length:", len(v4_as_list))
        # # 生成AS2Name的字典
        # as2name_dict = {}
        # for as_item in country_as_info:
        #     as2name_dict[as_item[0]] = as_item[1]
        # # 输出as-as name
        # as2name_v4_list = []
        # temp_as2name_list = []
        # for as_item in v4_as_list:
        #     print(as_item, as2name_dict[as_item])
        #     temp_as2name_list.append(as_item)
        #     temp_as2name_list.append(as2name_dict[as_item])
        #     as2name_v4_list.append(temp_as2name_list)
        #     temp_as2name_list = []
        # # 存储as2name_v4_list
        # save_path = "..\\000LocalData\\RUNet\\as2name_v4_list(CN).csv"
        # write_to_csv(as2name_v4_list, save_path)

        # 生成as_info_2_zf_Ping
        # as_info_2_zf_Ping = []
        # for item in country_as_info:
        #     if item[0] in external_as_list:
        #         as_info_2_zf_Ping.append(item[0:2])
        # print(as_info_2_zf_Ping)
        # # 存储as_info_2_zf_Ping
        # save_path = "..\\000LocalData\\RUNet\\as_info_2_zf_Ping.csv"
        # write_to_csv(as_info_2_zf_Ping, save_path)

        print("External Country Count:", len(list(set(external_country_list))))
        # print(list(set(external_country_list)))

        # 统计互联国家方向的排名
        external_country_rank = {}
        for item in list(set(external_country_list)):
            external_country_rank[item] = 0
        for item in external_country_list:
            external_country_rank[item] += 1
        # print(len(external_country_rank))
        # 将字典转为列表
        external_country_rank_list = []
        temp_list = []
        for item in external_country_rank.keys():
            temp_list.append(item)
            temp_list.append(external_country_rank[item])
            external_country_rank_list.append(temp_list)
            temp_list = []
        # print(external_country_rank_list)
        external_country_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        print(external_country_rank_list)
        # draw_bar(external_country_rank_list, country)


def draw_bar(rank_list, country):
    """
    根据传入的rank_list信息绘制直方图
    :param rank_list:
    :return:
    """
    x_list = []
    y_list = []

    for item in rank_list:
        x_list.append(item[0])
        y_list.append(item[1])
    # 开始绘图
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    title_string = "External BGP Relationships Analysis:" + country + "( Date:20200101 )"
    ax.set_title(title_string)
    color = ['blue']
    plt.bar(x_list, y_list, width=0.7, color=color)
    for x, y in zip(x_list, y_list):
        plt.text(x, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=11)
    ax.set_xlabel('Country')
    ax.set_ylabel('Relationships Nums')
    # plt.grid(True, linestyle=':', color='r', alpha=0.9)
    # plt.show()
    plt.savefig("..\\000LocalData\\RUNet\\External_BGP_Rel_" + country + ".jpg")


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = "CN"
    # as_info_file_in = '..\\000LocalData\\as_map\\as_core_map_data_new20200101.csv'
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    country_as_info, as2country_dict = gain_as2country(as_info_file_in, country)
    # print(country_as_info)
    # print(as2country_dict)
    external_as_analysis(country, country_as_info, as2country_dict)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
