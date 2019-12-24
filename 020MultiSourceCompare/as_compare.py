# coding:utf-8
"""
create on Dec 24 2019 By Wayne Yu
Function:

将Caida的AS BGP互联关系数据与高总的数据进行比对
以弥补，Caida数据在国内部分的缺失

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
    :return date_str:
    :return as_list:
    """
    # print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('\\')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        # print(line.strip())
        """
        每新增一个AS记录，就判断是否在AS列表中，在进行操作，耗时124s
        """
        # if line.strip().split('|')[0] not in as_list:
        #     as_list.append(line.strip().split('|')[0])
        # if line.strip().split('|')[1] not in as_list:
        #     as_list.append(line.strip().split('|')[1])
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    # print(as_list)
    # print("Active AS：", len(as_list))
    return date_str, as_list


def gain_as_country_dict():
    """
    返回国家和AS号的对应关系
    :param asn:
    :return country_info:
    """
    asn_info_file = '..\\000LocalData\\as_Gao\\asn_info.txt'
    asn_info_file_read = open(asn_info_file, 'r', encoding='utf-8')
    as_country_dict = {}
    for line in asn_info_file_read.readlines():
        line = line.strip().split("\t")
        as_country_dict[line[0]] = line[1].split(",")[-1].strip()
    return as_country_dict


def gain_as_rel_gao(file_gao):
    """
    将高总的文件，转换为AS|AS格式，以存储所有的边
    存在只有上游，没有下游的AS，如一些小型的ICP；应该不存在只有下游，没有上游的AS（包括transit和peer）
    即使向Level 3和HE这种大型的AS，至少都会存在Peer或者一个上游
    :param file_gao:
    :return as_rel_gao:
    """
    as_rel_gao = []
    temp_list = []

    file_gao_read = open(file_gao, 'r', encoding='utf-8')
    for line in file_gao_read.readlines():
        line = line.strip().split("\t")
        if len(line) == 2:  # 只有上游
            pass
        elif len(line) == 3:  # 上下游均有
            for downstream in line[2].split(","):
                temp_list.append(line[0])
                temp_list.append(downstream)
                as_rel_gao.append(temp_list)
                temp_list = []
    return as_rel_gao


def as_vertex_compare(as_caida_file, as_gao_file):
    """
    根据传入的Caida Source和Gao Source数据文件，分别绘制每个AS号的用户画像
    活跃AS号暂以Caida数据为主
    在Caida数据的基础之上，比对Gao数据，缺少的边（关系）则补录；冲突的边（关系），另行处理。

    Tips:在建立AS Stream 字典的时候，其实可以只存储下游

    :param as_caida_file:
    :param as_gao_file:
    :return:
    """
    print("Test Caida Source Data")
    # 根据Caida数据先行获取活跃的AS号
    date_string, active_as_list = gain_active_as(as_caida_file)
    print("Caida Source Active As:", len(active_as_list))
    # 根据as_caida_file文件，逐个建立上下游的AS画像字典
    as_caida_file_read = open(as_caida_file, 'r', encoding='utf-8')
    active_as_stream_dict_down = {}
    active_as_stream_dict_up = {}
    for line in as_caida_file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split("|")
        active_as_stream_dict_up.setdefault(line[1], []).append(line[0])
        active_as_stream_dict_down.setdefault(line[0], []).append(line[1])
    print("AS Up Stream Dict Length:", len(active_as_stream_dict_up.keys()))
    print("AS Down Stream Dict Length:", len(active_as_stream_dict_down.keys()))
    set_down = set(active_as_stream_dict_down.keys())
    set_up = set(active_as_stream_dict_up.keys())
    caida_as_set = set_down.union(set_up)
    print("AS Stream Set Union Length:", len(caida_as_set))  # 验证通过
    # print(active_as_stream_dict)
    print("- - - - - - - - - - - - - - - - - - - -")
    print("Test Gao Source Data")
    # 根据as_gao_file，逐个建立上下游的AS画像字典
    as_gao_file_read = open(as_gao_file, 'r', encoding='utf-8')
    line_cnt = 0
    as_gao_stream_dict_down = {}
    as_gao_stream_dict_up = {}
    for line in as_gao_file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        if len(line) == 2:  # 只有上游
            for item_as in line[1].split(","):
                as_gao_stream_dict_up.setdefault(line[0], []).append(item_as)
        elif len(line) == 3:  # 包含上下游
            for item_as in line[1].split(","):
                as_gao_stream_dict_up.setdefault(line[0], []).append(item_as)
            for item_as in line[2].split(","):
                as_gao_stream_dict_down.setdefault(line[0], []).append(item_as)
        else:
            print("ERROR:", line)
        line_cnt += 1
        # if line_cnt >= 10:
        #     break
    print("Gao File All lines:", line_cnt)
    print("AS Gao Stream Dict Up:", len(as_gao_stream_dict_up.keys()))
    print("AS Gao Stream Dict Down:", len(as_gao_stream_dict_down.keys()))
    set_down = set(as_gao_stream_dict_up.keys())
    set_up = set(as_gao_stream_dict_down.keys())
    gao_as_set = set_down.union(set_up)
    print("AS Gao Set Union Length:", len(gao_as_set))  # 验证通过
    print("- - - - - - - - - - - - - - - - - - - -")
    as_intersection = caida_as_set.intersection(gao_as_set)
    print("AS Intersection Length:", len(as_intersection))
    as_caida_difference = caida_as_set.symmetric_difference(as_intersection)
    print("AS Caida Difference Set Length:", len(as_caida_difference))
    as_gao_difference = gao_as_set.symmetric_difference(as_intersection)
    print("AS Gao Difference Set Length:", len(as_gao_difference))
    print("- - - - - - - - - - - - - - - - - - - -")
    # print(as_gao_difference)
    # print(gain_country_by_as("4134"))
    as_country_dict = gain_as_country_dict()
    # print(as_country_dict)
    cn_cnt = 0
    us_cnt = 0
    for as_item in as_gao_difference:
        try:
            if as_country_dict[as_item] == "CN":
                cn_cnt += 1
                # print("CN")
            if as_country_dict[as_item] == "US":
                us_cnt += 1
                # print("CN")
        except Exception as e:
            # print(e)
            pass

    print("As Gao diffence CN Count:", cn_cnt)
    print("As Gao diffence US Count:", us_cnt)



if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_in_caida = '..\\000LocalData\\as_relationships\\serial-1\\20191201.as-rel.txt'
    file_in_gao = '..\\000LocalData\\as_Gao\\asstream20191203.txt'
    file_in_gao_format = '..\\000LocalData\\as_Gao\\as_rel_gao_20191203.txt'
    # as_gao_list = gain_as_rel_gao(file_in_gao)
    # print(as_gao_list)
    as_vertex_compare(file_in_caida, file_in_gao)
    # save_path = '..\\000LocalData\\as_Gao\\as_rel_gao_20191203.txt'
    # write_to_csv(as_gao_list, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
