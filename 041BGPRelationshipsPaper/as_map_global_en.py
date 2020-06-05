# coding: utf-8
"""
create on May 6, 2020 By Wayne YU

Version: 1.0
Description:

通过这么些时间沉淀，要开始成果的输出了，上一轮是俄罗斯断网事件，这一轮要重点研究国内AS网络，越细越好
包括国内互联情况、与国外的互联情况，有条件有深入研究每个AS号
目前手头的AS互联数据可以一窥国内互联网的总体现状
并以此为抓手，不断扩充内容

该程序用于实现基于Caida、Gao及其intergrate的数据，实现国内AS号网络画像的构建
时间以2020年2月21日的数据为准


生成画像字段为
asn, all rel , peer, train as provider, train as customer, internal rel, external rel, org name , country

Version:2.0

更换生成画像的字段，应包含经纬度信息


Version:3.0
为了地图基础课题第一篇论文输出，重新绘图，使得排版更加美观
绘制时间修改为19980101-20191201

"""

import time
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
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


def gain_active_as(open_file):
    """
    根据输入的AS互联关系数据，获取当前时间活跃的AS列表
    :param open_file:
    :return:
    """
    print(open_file)
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    rel_num = 0
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        """
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
        rel_num += 1
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    return as_list, rel_num


def gain_as_relationships_dict(asn_list, open_file):
    """
    根据传入的asn_list,统计其bgp互联关系(All, Peer, Transit)
    :param asn_list:
    :param open_file:
    :return rel:
    """
    as_rel_dict = {}  # 存储as互联关系统计结果
    # 根据asn_list生成原始字典
    # 构造原始字典中的list时，有一定的讲究，否则就是个坑
    # dict_value = [0, 0, 0, 0]  # edge_cnt、peer_cnt、transit_provider_cnt、transit_customer_cnt
    for asn_item in asn_list:
        as_rel_dict.setdefault(asn_item, []).append(0)
        as_rel_dict.setdefault(asn_item, []).append(0)
        as_rel_dict.setdefault(asn_item, []).append(0)
        as_rel_dict.setdefault(asn_item, []).append(0)
    # 遍历bgp互联关系列表，统计as互联关系
    file_read = open(open_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        # print(line)
        if len(line) == 3:  # 如果为三元组
            if line[2] == '0':  # 如果该条关系为peer的关系
                # print("Peer")
                # 总连接数自增1
                as_rel_dict[line[0]][0] += 1
                as_rel_dict[line[1]][0] += 1
                # Peer连接数自增1
                as_rel_dict[line[0]][1] += 1
                as_rel_dict[line[1]][1] += 1
            elif line[2] == '-1':  # 否则该条关系为transit关系
                # print("Transit")
                # 总连接数自增1
                as_rel_dict[line[0]][0] += 1
                as_rel_dict[line[1]][0] += 1
                # provider-customer，transit关系分别自增1
                as_rel_dict[line[0]][2] += 1
                as_rel_dict[line[1]][3] += 1
            # print(as_rel_dict)
        else:  # 如果为二元组
            # 总连接数自增1
            as_rel_dict[line[0]][0] += 1
            as_rel_dict[line[1]][0] += 1
            # print(as_rel_dict)

    return as_rel_dict


def gain_as_info(as_list):
    """
    根据传入的as list，集合asn_info.txt，获取其as 的详细信息，包括as_org as_country
    :param as_list:
    :return as_list:
    """
    as_org_info_file = "..\\000LocalData\\as_geo\\as_org_info.csv"
    as_org_info_file_read = open(as_org_info_file, 'r', encoding='utf-8')
    # 读取以便as_org_info_file，用哈希表的方式记录其信息
    as_org_info_dict = {}

    for line in as_org_info_file_read.readlines():
        line = line.strip().split("|")
        as_org_info_dict.setdefault(line[0], []).append(line[2])
        as_org_info_dict.setdefault(line[0], []).append(line[3])
        as_org_info_dict.setdefault(line[0], []).append(line[5])
        as_org_info_dict.setdefault(line[0], []).append(line[4])
        as_org_info_dict.setdefault(line[0], []).append(line[6])
        as_org_info_dict.setdefault(line[0], []).append(line[7])

    # for line in as_org_info_file_read.readlines():
    #     line = line.strip().split("\t")
    #     as_org = ""
    #     for item in line[1].strip().split(",")[0: -1]:
    #         as_org = as_org + item
    #     as_country = line[1].strip().split(",")[-1].strip()
    #     as_org_info_dict.setdefault(line[0], []).append(as_org)
    #     as_org_info_dict.setdefault(line[0], []).append(as_country)

    # print(as_org_info_dict)
    # 根据as org info哈希表，生成asn_core_map_list信息
    except_as = []  # 存储没有信息的asn
    as_list_copy = []
    for item in as_list:
        try:
            item.extend(as_org_info_dict[item[0]])
            as_list_copy.append(item)
        except Exception as e:
            # print(e, item[0])
            except_as.append(item[0])
    # 输出没有信息的asn号
    print("没有信息的asn号个数:", len(set(except_as)))
    # print(set(except_asn))
    as_list = as_list_copy
    return as_list


def draw_bar(data_list):
    """
    对传入的数据进行绘图
    :param draw_date:
    :param data_list:
    :return:
    """
    # print(data_list)
    x_list = []
    y_list = []

    for item in data_list:
        x_list.append(item[0])
        y_list.append(item[1])

    # 开始绘图
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
    # tick_spacing = 12
    # title_string = "全球TOP10自治系统网络（2019）"
    # ax.set_title(title_string, font)
    color = ['blue']
    plt.bar(x_list, y_list, width=0.7, color=color)
    for x, y in zip(x_list, y_list):
        plt.text(x, y + 0.05, '%.0f' % y, ha='center', va='bottom', fontsize=32)
    ax.set_xlabel('Time of estimation', font)
    ax.set_ylabel('Network degree', font)
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.grid(True)
    fig.tight_layout()
    plt.savefig("..\\000LocalData\\Paper_Data\\draw_top10as_en.jpg", dpi=1080)


def get_as_classification_dict():
    """
    根据as classification文件内容对AS进行分类，返回分类字典
    :return as_class_dict:
    """
    file_in = "..\\000LocalData\\as_Classification\\20190901.as2types.txt"
    file_in_read = open(file_in, 'r', encoding='utf-8')
    as_class_dict = {}
    for line in file_in_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        as_class_dict[line[0]] = line[2]
    return as_class_dict


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    time_string = "20191201"
    rel_file_caida = "..\\000LocalData\\as_relationships\\serial-4\\" + time_string + ".as-rel.txt"
    save_path_home = "..\\000LocalData\\Paper_Data\\"

    # 数据源CIADA
    print("=>CAIDA数据源")
    caida_as_list, caida_rel = gain_active_as(rel_file_caida)
    print("Caida Active AS Num（%s），Rel（%s） " % (len(caida_as_list), caida_rel))
    # 获取CAIDA数据源互联关系字典
    as_rel_dict_caida = gain_as_relationships_dict(caida_as_list, rel_file_caida)
    # print(as_rel_dict_caida)

    # 遍历as_rel_dict_caida 生成as_map_caida
    as_map_caida = []
    list_temp = []
    for key in as_rel_dict_caida:
        list_temp.append(key)
        list_temp.extend(as_rel_dict_caida[key])
        as_map_caida.append(list_temp)
        list_temp = []
    as_map_caida.sort(reverse=False, key=lambda elem: int(elem[0]))
    as_map_caida = gain_as_info(as_map_caida)
    # 存储as_map文件
    save_path = save_path_home + 'as_map_caida_' + time_string + '.csv'
    write_to_csv(as_map_caida, save_path)
    # 存储rank数据
    save_path = save_path_home + 'as_map_caida_' + time_string + '_Rank.csv'
    as_map_caida.sort(reverse=True, key=lambda elem: int(elem[1]))
    write_to_csv(as_map_caida, save_path)
    as_class_dict = get_as_classification_dict()
    # print(as_class_dict)

    # 对全球TOP10互联网络服务商进行度的统计，并绘图
    top_as_rel = []
    list_temp = []
    sum_degreee = 0
    top3_sum_degreee = 0
    cnt = 0
    for item in as_map_caida[0:10]:
        if cnt < 3:
            top3_sum_degreee += int(item[1])
        sum_degreee += int(item[1])

        if item[0] not in as_class_dict.keys():
            print(item[0], item[6], item[1])
            temp_str = "AS" + str(item[0])
            list_temp.append(temp_str)
            list_temp.append(item[1])
            list_temp.append("Unknow")
        else:
            print(item[0], item[6], item[1], as_class_dict[item[0]])
            temp_str = "AS" + str(item[0])
            list_temp.append(temp_str)
            list_temp.append(item[1])
            list_temp.append(as_class_dict[item[0]])
        top_as_rel.append(list_temp)
        list_temp = []
        cnt += 1
    # print(top_as_rel)
    print("TOP3 percent:", (top3_sum_degreee/sum_degreee))
    # 绘图
    draw_bar(top_as_rel)
    # 统计自治域网络的分类（Transit/Access、Content、Enterprise）
    class_count_dict = {}
    for item in top_as_rel:
        if item[2] not in class_count_dict.keys():
            class_count_dict[item[2]] = 1
        else:
            class_count_dict[item[2]] += 1
    print(class_count_dict)

    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")