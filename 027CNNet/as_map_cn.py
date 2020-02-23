# coding: utf-8
"""
create on Feb 21, 2020 By Wayne YU

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

"""

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
    as_org_info_file = "..\\000LocalData\\as_Gao\\asn_info.txt"
    # as_org_info_file = "..\\000LocalData\\as_geo\\as_org_info.csv"
    as_org_info_file_read = open(as_org_info_file, 'r', encoding='utf-8')
    # 读取以便as_org_info_file，用哈希表的方式记录其信息
    as_org_info_dict = {}

    # for line in as_org_info_file_read.readlines():
    #     line = line.strip().split("|")
    #     as_org_info_dict.setdefault(line[0], []).append(line[1])
    #     as_org_info_dict.setdefault(line[0], []).append(line[2])
    #     as_org_info_dict.setdefault(line[0], []).append(line[5])
    #     as_org_info_dict.setdefault(line[0], []).append(line[4])
    #     as_org_info_dict.setdefault(line[0], []).append(line[6])
    #     as_org_info_dict.setdefault(line[0], []).append(line[7])

    for line in as_org_info_file_read.readlines():
        line = line.strip().split("\t")
        as_org = ""
        for item in line[1].strip().split(",")[0: -1]:
            as_org = as_org + item
        as_country = line[1].strip().split(",")[-1].strip()
        as_org_info_dict.setdefault(line[0], []).append(as_org)
        as_org_info_dict.setdefault(line[0], []).append(as_country)

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


def gain_as_info_country(as_list, open_file, country):
    """
    根据传入as_list及互联关系文件，统计该国每个AS号国内和国际互联的数量
    :param as_list:
    :param open_file:
    :return as_list:
    """
    as2country = {}  # 生成as2country字典
    for item in as_list:
        as2country[item[0]] = item[-1]

    as_rel_dict = {}  # 存储as互联关系统计结果，国内互联和国际互联
    for item in as_list:
        as_rel_dict.setdefault(item[0], []).append(0)  # 存储国内互联
        as_rel_dict.setdefault(item[0], []).append(0)  # 存储国际互联

    # 遍历BGP互联关系列表，统计其as互联关系
    file_read = open(open_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        try:
            if as2country[line[0]] != country and as2country[line[1]] != country:
                continue
            else:
                if as2country[line[0]] == country and as2country[line[1]] == country:
                    # 国内互联
                    as_rel_dict[line[0]][0] += 1
                    as_rel_dict[line[1][0]] += 1
                elif as2country[line[0]] == country and as2country[line[1]] != country:
                    # line[0]国际互联
                    as_rel_dict[line[0]][1] += 1
                elif as2country[line[1]] == country and as2country[line[0]] != country:
                    # line[1]国际互联
                    as_rel_dict[line[1]][1] += 1
        except Exception as e:
            # print(e)
            pass
    # 生成as_list_cn
    as_list_cn = []
    temp_list = []
    for item in as_list:
        if item[6] == country:
            temp_list.extend(item[0:2])
            temp_list.append(as_rel_dict[item[0]][0])
            temp_list.append(as_rel_dict[item[0]][1])
            temp_list.extend(item[5:])
            as_list_cn.append(temp_list)
            temp_list = []
    return as_list_cn


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    country = "CN"  # 分析的国家缩写
    rel_file_caida = "..\\000LocalData\\as_relationships\\serial-1\\20200201.as-rel.txt"
    rel_file_gao = "..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt"
    rel_file_intergrate = "..\\000LocalData\\as_compare\\as_rel_20200221_integrate.txt"

    # 数据源CIADA
    print("\n=>CAIDA数据源")
    caida_as_list, caida_rel = gain_active_as(rel_file_caida)
    print("Caida Active AS Num（%s），Rel（%s） " % (len(caida_as_list), caida_rel))
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
    save_path = '..\\000LocalData\\as_cn\\as_map_caida_20200221.csv'
    write_to_csv(as_map_caida, save_path)
    # 存储rank数据
    save_path = '..\\000LocalData\\as_cn\\as_map_caida_20200221_Rank.csv'
    as_map_caida.sort(reverse=True, key=lambda elem: int(elem[1]))
    write_to_csv(as_map_caida, save_path)
    # 生成as_map_cn数据，并存储
    as_map_cn_caida = gain_as_info_country(as_map_caida, rel_file_caida, country)
    as_map_cn_caida.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_path = '..\\000LocalData\\as_cn\\as_map_caida_20200221_cn.csv'
    write_to_csv(as_map_cn_caida, save_path)
    # 生成as_map_cn数据Rank，并存储
    as_map_cn_caida.sort(reverse=True, key=lambda elem: int(elem[1]))
    save_path = '..\\000LocalData\\as_cn\\as_map_caida_20200221_Rank_cn.csv'
    write_to_csv(as_map_cn_caida, save_path)

    # 数据源Gao
    print("\n=>Gao数据源")
    gao_as_list, gao_rel = gain_active_as(rel_file_gao)
    print("Gao Active AS Num（%s），Rel（%s）" % (len(gao_as_list), gao_rel))
    as_rel_dict_gao = gain_as_relationships_dict(gao_as_list, rel_file_gao)
    # print(as_rel_dict_gao)
    # 遍历as_rel_dict 生成as_map
    as_map_gao = []
    list_temp = []
    for key in as_rel_dict_gao:
        list_temp.append(key)
        list_temp.extend(as_rel_dict_gao[key])
        as_map_gao.append(list_temp)
        list_temp = []
    as_map_gao.sort(reverse=False, key=lambda elem: int(elem[0]))
    as_map_gao = gain_as_info(as_map_gao)
    # 存储as_map文件
    save_path = '..\\000LocalData\\as_cn\\as_map_gao_20200221.csv'
    write_to_csv(as_map_gao, save_path)
    # 存储rank数据
    save_path = '..\\000LocalData\\as_cn\\as_map_gao_20200221_Rank.csv'
    as_map_gao.sort(reverse=True, key=lambda elem: int(elem[1]))
    write_to_csv(as_map_gao, save_path)
    # 生成as_map_cn数据，并存储
    as_map_cn_gao = gain_as_info_country(as_map_gao, rel_file_gao, country)
    as_map_cn_gao.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_path = '..\\000LocalData\\as_cn\\as_map_gao_20200221_cn.csv'
    write_to_csv(as_map_cn_gao, save_path)
    # 生成as_map_cn数据Rank，并存储
    as_map_cn_gao.sort(reverse=True, key=lambda elem: int(elem[1]))
    save_path = '..\\000LocalData\\as_cn\\as_map_gao_20200221_Rank_cn.csv'
    write_to_csv(as_map_cn_gao, save_path)

    # 数据源Intergrate
    print("\n=>Intergrate数据源")
    intergrate_as_list, intergrate_rel = gain_active_as(rel_file_intergrate)
    print("Intergrate Active AS Num（%s），Rel（%s）" % (len(intergrate_as_list), intergrate_rel))
    as_rel_dict_intergrate = gain_as_relationships_dict(intergrate_as_list, rel_file_intergrate)
    # print(as_rel_dict_intergrate)
    # 遍历as_rel_dict 生成as_map
    as_map_intergrate = []
    list_temp = []
    for key in as_rel_dict_intergrate:
        list_temp.append(key)
        list_temp.extend(as_rel_dict_intergrate[key])
        as_map_intergrate.append(list_temp)
        list_temp = []
    as_map_intergrate.sort(reverse=False, key=lambda elem: int(elem[0]))
    as_map_intergrate = gain_as_info(as_map_intergrate)
    # 存储as_map文件
    save_path = '..\\000LocalData\\as_cn\\as_map_intergrate_20200221.csv'
    write_to_csv(as_map_intergrate, save_path)
    # 存储rank数据
    save_path = '..\\000LocalData\\as_cn\\as_map_intergrate_20200221_Rank.csv'
    as_map_intergrate.sort(reverse=True, key=lambda elem: int(elem[1]))
    write_to_csv(as_map_intergrate, save_path)
    # 生成as_map_cn数据，并存储
    as_map_cn_intergrate = gain_as_info_country(as_map_intergrate, rel_file_intergrate, country)
    as_map_cn_intergrate.sort(reverse=False, key=lambda elem: int(elem[0]))
    save_path = '..\\000LocalData\\as_cn\\as_map_intergrate_20200221_cn.csv'
    write_to_csv(as_map_cn_intergrate, save_path)
    # 生成as_map_cn数据Rank，并存储
    as_map_cn_intergrate.sort(reverse=True, key=lambda elem: int(elem[1]))
    save_path = '..\\000LocalData\\as_cn\\as_map_intergrate_20200221_Rank_cn.csv'
    write_to_csv(as_map_cn_intergrate, save_path)

    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")