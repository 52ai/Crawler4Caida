# coding:utf-8
"""
create on Feb 12, 2020 By Wayne YU

Function:

V2：
在研究俄罗斯断网事件的过程，对出口AS网络做了详细的研究
需进一步分析，我国出口AS互联关系中，美国占比的情况
分为两类，一类是全部互联关系；一类是AS TOP 1000的互联关系占比情况



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
        # 统计出口AS的排名
        external_as_rank = {}
        for item in list(set(external_as_list)):
            external_as_rank[item] = 0
        for item in external_as_list:
            external_as_rank[item] += 1
        # 将字典转换为列表
        external_as_rank_list = []
        temp_list = []
        for item in external_as_rank.keys():
            temp_list.append(item)
            temp_list.append(external_as_rank[item])
            external_as_rank_list.append(temp_list)
            temp_list = []
        external_as_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))
        external_as_list = list(set(external_as_list))
        print("All External Edges Count:", external_cnt)
        print("All External AS Count:", len(external_as_list))
        print(external_as_rank_list)

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

        print("All External Country Count:", len(list(set(external_country_list))))
        # print(list(set(external_country_list)))

        # 统计互联国家方向的排名
        external_country_rank = {}
        for item in list(set(external_country_list)):
            external_country_rank[item] = 0
        for item in external_country_list:
            external_country_rank[item] += 1
        # print(len(external_country_rank))
        # print(external_country_rank["US"])

        # 统计中国出口AS互联关系中美国、俄罗斯、日本、中国香港的占比
        print("All External Edges  （US）: %s, %f%%" % (external_country_rank["US"], float(external_country_rank["US"]/external_cnt) * 100))
        print("All External Edges  （RU）: %s, %f%%" % (external_country_rank["RU"], float(external_country_rank["RU"]/external_cnt) * 100))
        print("All External Edges  （JP）: %s, %f%%" % (external_country_rank["JP"], float(external_country_rank["JP"]/external_cnt) * 100))
        print("All External Edges  （HK）: %s, %f%%" % (external_country_rank["HK"], float(external_country_rank["HK"]/external_cnt) * 100))

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
        draw_bar(external_country_rank_list, country)


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
    fig, ax = plt.subplots(1, 1, figsize=(50, 10))
    title_string = "External BGP Relationships Analysis:" + country + "( Date:20200201 )"
    ax.set_title(title_string)
    color = ['blue']
    plt.bar(x_list, y_list, width=0.7, color=color)
    for x, y in zip(x_list, y_list):
        plt.text(x, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=11)
    ax.set_xlabel('Country')
    ax.set_ylabel('Relationships Nums')
    # plt.grid(True, linestyle=':', color='r', alpha=0.9)
    # plt.show()
    plt.savefig("..\\000LocalData\\RUNet\\External_BGP_Rel_" + country + "(20200201).jpg")


def external_as_analysis_topn(topn, country, country_as_info, as2country, as_info_topn):
    """
    根据传入的信息，计算当前国家出口AS与TOP N AS互联关系中，各主要国家的占比情况
    :param topn:
    :param country:
    :param country_as_info:
    :param as2country_dict:
    :param as_info_topn:
    :return:
    """
    # 先求出topn的AS号列表
    global_as_info = []  # 存储全球 as 信息
    file_read_topn = open(as_info_topn, 'r', encoding='utf-8')
    for line in file_read_topn.readlines():
        line = line.strip().split("|")
        global_as_info.append(line)
    global_as_info.sort(reverse=True, key=lambda  elem: int(elem[1]))
    top_n_as_info = global_as_info[0:topn]
    top_n_as_list = []  # 存储所有topn的as
    for item_as in top_n_as_info:
        top_n_as_list.append(item_as[0])
    # print(top_n_as_list)

    # 获取1998-2020年全球BGP互联关系的存储文件
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))

    for path_item in file_path[-1:]:
        print(path_item)
        # 遍历一次文件，获取该国与TOP N AS的互联关系点数与边数
        file_read = open(path_item, 'r', encoding='utf-8')
        top_n_external_cnt = 0  # 存储该国与TOP N AS，出口互联边的数量
        top_n_external_as_list = []  # 存储该国与TOP N AS互联的出口AS
        top_n_external_country_list = []  # 存储该国与TOP N AS互联，出口方向的国家
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if as2country[str(line.strip().split('|')[0])] == country:
                    if as2country[str(line.strip().split('|')[1])] != country:
                        if str(line.strip().split('|')[1]) in top_n_as_list:
                            top_n_external_cnt += 1
                            top_n_external_as_list.append(str(line.strip().split('|')[0]))
                            top_n_external_country_list.append(str(as2country[line.strip().split('|')[1]]))
                else:
                    if as2country[str(line.strip().split('|')[1])] == country:
                        if str(line.strip().split('|')[0]) in top_n_as_list:
                            top_n_external_cnt += 1
                            top_n_external_as_list.append(str(line.strip().split('|')[1]))
                            top_n_external_country_list.append(str(as2country[line.strip().split('|')[0]]))
            except Exception as e:
                pass
        # 统计出口AS的排名
        external_as_rank = {}
        for item in list(set(top_n_external_as_list)):
            external_as_rank[item] = 0
        for item in top_n_external_as_list:
            external_as_rank[item] += 1
        # 将字典转换为列表
        external_as_rank_list = []
        temp_list = []
        for item in external_as_rank.keys():
            temp_list.append(item)
            temp_list.append(external_as_rank[item])
            external_as_rank_list.append(temp_list)
            temp_list = []
        external_as_rank_list.sort(reverse=True, key=lambda elem: int(elem[1]))

        top_n_external_as_list = list(set(top_n_external_as_list))
        print("<TOP %s AS>External Edges Count: %s" % (topn, top_n_external_cnt))
        print("<TOP %s AS>External AS Count: %s" % (topn, len(top_n_external_as_list)))
        print(external_as_rank_list)
        print("<TOP %s AS>External Counter Count: %s" % (topn, len(list(set(top_n_external_country_list)))))

        # 统计互联国家方向排名
        external_country_rank = {}
        for item in list(set(top_n_external_country_list)):
            external_country_rank[item] = 0
        for item in top_n_external_country_list:
            external_country_rank[item] += 1

        # 统计中国出口AS互联关系中美国、俄罗斯、日本、中国香港的占比
        print("<TOP %s AS>External Edges  （US）: %s, %f%%" % (topn, external_country_rank["US"], float(external_country_rank["US"] / top_n_external_cnt) * 100))
        print("<TOP %s AS>External Edges  （RU）: %s, %f%%" % (topn, external_country_rank["RU"], float(external_country_rank["RU"] / top_n_external_cnt) * 100))
        print("<TOP %s AS>External Edges  （US）: %s, %f%%" % (topn, external_country_rank["JP"], float(external_country_rank["JP"] / top_n_external_cnt) * 100))
        print("<TOP %s AS>External Edges  （HK）: %s, %f%%" % (topn, external_country_rank["HK"], float(external_country_rank["HK"] / top_n_external_cnt) * 100))
        # 将字典转换为列表
        external_country_rank_list = []
        temp_list = []
        for item in external_country_rank.keys():
            temp_list.append(item)
            temp_list.append(external_country_rank[item])
            external_country_rank_list.append(temp_list)
            temp_list = []
        external_country_rank_list.sort(reverse=True, key=lambda elem:int(elem[1]))
        print(external_country_rank_list)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = "CN"
    as_info_file_top = '..\\000LocalData\\as_map\\as_core_map_data_new20200201.csv'
    top_n = 1000
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    country_as_info, as2country_dict = gain_as2country(as_info_file_in, country)
    # print(country_as_info)
    # print(as2country_dict)
    external_as_analysis(country, country_as_info, as2country_dict)
    print("- - - - - - - - - - - - line- - - - - - - - - - - - - - - - - - ")
    external_as_analysis_topn(top_n, country, country_as_info, as2country_dict, as_info_file_top)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
