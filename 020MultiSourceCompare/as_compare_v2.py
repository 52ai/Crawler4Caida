# coding:utf-8
"""
create on Feb 21 2020 By Wayne Yu
Function:

将Caida的AS BGP互联关系数据与高总的数据进行比对
以弥补，Caida数据在国内部分的缺失

V2:

采用最新数据2200221
根据高总的数据生成Caida格式的互联关系
将Caida的AS BGP互联数据与高总的数据进行对比

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


def gain_as_rel_gao(file_gao):
    """
    将高总的文件，转换为AS|AS格式，以存储所有的边
    存在只有上游，没有下游的AS，如一些小型的ICP；应该不存在只有下游，没有上游的AS（包括transit和peer）
    即使向Level 3和HE这种大型的AS，至少都会存在Peer或者一个上游
    一句话概括“一个AS网络，若只存在一条边（关系），那一定是作为下游。”
    :param file_gao:
    :return as_rel_gao:
    """
    as_rel_gao = []
    temp_list = []

    file_gao_read = open(file_gao, 'r', encoding='utf-8')
    for line in file_gao_read.readlines():
        line = line.strip().split("\t")
        if len(line) == 2:  # 只有上游
            for upstream in line[1].split(","):
                temp_list.append(upstream)
                temp_list.append(line[0])
                as_rel_gao.append(temp_list)
                temp_list = []
        elif len(line) == 3:  # 上下游均有
            for downstream in line[2].split(","):
                temp_list.append(line[0])
                temp_list.append(downstream)
                as_rel_gao.append(temp_list)
                temp_list = []
            for upstream in line[1].split(","):
                temp_list.append(upstream)
                temp_list.append(line[0])
                as_rel_gao.append(temp_list)
                temp_list = []
    # 至此Gao的数共有84万条边，这其中有被重复计算2遍的Peer边。理论上，这种边只需要计算一次，因此需要去重
    # 通过去重的步骤，其实是可以大致确定其BGP互联关系，互为上下游则为Peer，单向的为Transit，上游为Provider，下游为Customer
    # 设计一个去重算法，尽可能的降低时间复杂度

    as_rel_gao_return = []  # 存储最终返回的AS 互联关系数据
    as_rel_gao_inner = as_rel_gao  # 存储去重前的AS互联关系数据，作为内循环
    find_cnt = 0  # 存储当前关系在as_rel_gao_inner中出现的次数
    find_flag = []  # 存储出现相同关系的此处，有三种情况0次（Transit）,2次（Peer）,1次（as_rel_gao_inner删除靠前重复项之后）
    for item in as_rel_gao:
        print("当前行记录：", item)
        find_item_index = 0  # 初始化内循环计数器
        for find_item in as_rel_gao_inner:
            if item[0] == find_item[1] and item[1] == find_item[0]:
                print("当前行记录与匹配行记录:", item[0], item[1], find_item[0], find_item[1])
                find_flag.append(find_item_index)
                find_cnt += 1
            find_item_index += 1
        print("边重复出现的次数(上下游翻转):", find_cnt)
        if find_cnt == 0:
            item.append('-1')
            print("准备添加的Item:", item)
            as_rel_gao_return.append(item)
        elif find_cnt == 1:
            item.append('0')
            print("准备添加的Item:", item)
            as_rel_gao_return.append(item)
        elif find_cnt == 2:
            print("边重复在内循环列表的index：",find_flag)
            item.append('0')
            del as_rel_gao_inner[find_flag[0]]
            print("内循环列表的长度:", len(as_rel_gao_inner))
        else:
            print("Attention!")

        find_cnt = 0
        find_flag = []

    return as_rel_gao


def gain_as_rel_gao_v2(file_gao):
    """
    将高总的文件，转换为AS|AS格式，以存储所有的边
    存在只有上游，没有下游的AS，如一些小型的ICP；应该不存在只有下游，没有上游的AS（包括transit和peer）
    即使向Level 3和HE这种大型的AS，至少都会存在Peer或者一个上游
    一句话概括“一个AS网络，若只存在一条边（关系），那一定是作为下游。”
    V2版本，优化去重的算法
    :param file_gao:
    :return as_rel_gao:
    """
    as_rel_gao = []
    temp_list = []

    file_gao_read = open(file_gao, 'r', encoding='utf-8')
    for line in file_gao_read.readlines():
        line = line.strip().split("\t")
        if len(line) == 2:  # 只有上游
            for upstream in line[1].split(","):
                temp_list.append(upstream)
                temp_list.append(line[0])
                as_rel_gao.append(temp_list)
                temp_list = []
        elif len(line) == 3:  # 上下游均有
            for downstream in line[2].split(","):
                temp_list.append(line[0])
                temp_list.append(downstream)
                as_rel_gao.append(temp_list)
                temp_list = []
            for upstream in line[1].split(","):
                temp_list.append(upstream)
                temp_list.append(line[0])
                as_rel_gao.append(temp_list)
                temp_list = []
    # 至此Gao的数共有84万条边，这其中有被重复计算2遍的Peer边。理论上，这种边只需要计算一次，因此需要去重
    # 通过去重的步骤，其实是可以大致确定其BGP互联关系，互为上下游则为Peer，单向的为Transit，上游为Provider，下游为Customer
    # 设计一个去重算法，尽可能的降低时间复杂度
    as_rel_gao_str = []
    for item in as_rel_gao:
        item_str = item[0] + "|" + item[1]
        as_rel_gao_str.append(item_str)
    print(len(as_rel_gao_str))

    return as_rel_gao


def gain_as_rel_gao_v3(as_gao_stream_dict_up):
    """
    将根据高总文件生成的用户上下游画像，转换为AS|AS的关系数据
    :param as_gao_stream_dict_up:
    :return :
    """
    as_rel_gao = []
    temp_list = []
    key_cnt = 0
    for key in as_gao_stream_dict_up.keys():
        # print(key, as_gao_stream_dict[key])
        for upas in as_gao_stream_dict_up[key]:
            if len(upas) == 0:
                continue
            temp_list.append(upas)
            temp_list.append(key)
            # print(temp_list)
            as_rel_gao.append(temp_list)
            temp_list = []
        key_cnt += 1
        # if key_cnt > 10:
        #     break
    # 对 as_rel_gao列表按照，item[0]进行排序
    as_rel_gao.sort(key=lambda elem:int(elem[0]))
    save_path = '..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_up.txt'
    write_to_csv(as_rel_gao, save_path)


def gain_as_rel_gao_v4(as_gao_stream_dict_down):
    """
    将根据高总文件生成的用户上下游画像，转换为AS|AS的关系数据
    :param as_gao_stream_dict_down:
    :return :
    """
    as_rel_gao = []
    temp_list = []
    key_cnt = 0
    for key in as_gao_stream_dict_down.keys():
        # print(key, as_gao_stream_dict[key])
        for downas in as_gao_stream_dict_down[key]:
            temp_list.append(key)
            temp_list.append(downas)
            # print(temp_list)
            as_rel_gao.append(temp_list)
            temp_list = []
        key_cnt += 1
        # if key_cnt > 10:
        #     break

    save_path = '..\\000LocalData\\as_Gao\\as_rel_gao_20200221_dict_down.txt'
    write_to_csv(as_rel_gao, save_path)


def gain_as_rel_integrate(as_rel_list):
    """
    根据传输的as_rel_list进行排序、去重处理
    :param as_rel_list:
    :return :
    """
    print("处理并获取AS_Rel文件")

    print("去重前的列表长度:", len(as_rel_list))
    as_rel_list.sort(key=lambda elem:int(elem[0]))  # 按照上游AS号进行排序
    # 对排序后的AS号进行去重操作
    as_rel_list_result = []
    item_cnt = 0
    flag = as_rel_list[0][0]
    group_list = []  # 存储组内list，进行去重操作
    temp_list = []
    for item in as_rel_list:
        if flag == item[0]:
            group_list.append(item[1])
        else:
            group_list = list(set(group_list))
            group_list.sort(key=lambda elem:int(elem))
            for downas in group_list:
                temp_list.append(flag)
                temp_list.append(downas)
                # print(temp_list)
                as_rel_list_result.append(temp_list)
                temp_list = []
            flag = item[0]  # 重置flag
            group_list = []  # 重置组内存储list
        # if item_cnt > 100:
        #     break
        item_cnt += 1
    print("去重后的列表长度:", len(as_rel_list_result))
    save_path = '..\\000LocalData\\as_compare\\as_rel_20200221_integrate.txt'
    write_to_csv(as_rel_list_result, save_path)


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


def as_vertex_compare(as_caida_file, as_gao_file):
    """
    根据传入的Caida Source和Gao Source数据文件，分别绘制每个AS号的用户画像
    活跃AS号暂以Caida数据为主
    在Caida数据的基础之上，比对Gao数据，缺少的边（关系）则补录；冲突的边（关系）(最多反向)，另行处理。

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
    # print(active_as_stream_dict_down)
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
    print("as2country Dict Length:", len(as_country_dict))
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
    print("- - - - - - - - - - - - - - - - - - - -")
    # print(as_gao_stream_dict_up)
    # gain_as_rel_gao_v3(as_gao_stream_dict_up)  # 根据生成自治域网络画像字典，生成AS|AS格式文件(上游)
    # gain_as_rel_gao_v4(as_gao_stream_dict_down) # 根据生成自治域网络画像字典，生成AS|AS格式文件（下游）

    # 将高总的数据和Caida的数据进行整合
    # 先搞一个最全的，然后排序，再进行去重

    as_rel_integrate_list = []  # 存储边的关系合集
    temp_list = []
    print("根据自治域网络画像字典生成边的关系集合")
    # 根据Caida Data的下游字典生成边的关系
    # print("根据Caida Data的下游字典生成边的关系")
    for key in active_as_stream_dict_down.keys():
        for downas in active_as_stream_dict_down[key]:
            if len(downas) == 0:
                continue
            temp_list.append(key)
            temp_list.append(downas)
            as_rel_integrate_list.append(temp_list)
            temp_list = []
    # print(len(as_rel_integrate_list))
    # 根据Gao Data的下游字典生成边的关系
    # print("根据Gao Data的下游字典生成边的关系")
    for key in as_gao_stream_dict_down.keys():
        for downas in as_gao_stream_dict_down[key]:
            if len(downas) == 0:
                continue
            temp_list.append(key)
            temp_list.append(downas)
            as_rel_integrate_list.append(temp_list)
            temp_list = []
    # print(len(as_rel_integrate_list))
    # 根据Caida Data的上游字典生成边的关系
    # print("根据Caida Data的上游字典生成边的关系")
    for key in active_as_stream_dict_up.keys():
        for upas in active_as_stream_dict_up[key]:
            if len(upas) == 0:
                continue
            temp_list.append(upas)
            temp_list.append(key)
            as_rel_integrate_list.append(temp_list)
            temp_list = []
    # print(len(as_rel_integrate_list))
    # 根据Gao Data的上游字典生成边的关系
    # print("根据Gao Data的上游字典生成边的关系")
    for key in as_gao_stream_dict_up.keys():
        for upas in as_gao_stream_dict_up[key]:
            if len(upas) == 0:
                continue
            temp_list.append(upas)
            temp_list.append(key)
            as_rel_integrate_list.append(temp_list)
            temp_list = []
    # print(len(as_rel_integrate_list))
    gain_as_rel_integrate(as_rel_integrate_list)  # 根据as rel 列表生成文件


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    file_in_caida = '..\\000LocalData\\as_relationships\\serial-1\\20200201.as-rel.txt'
    file_in_gao = '..\\000LocalData\\as_Gao\\asstream20200221.txt'
    # file_in_gao_format = '..\\000LocalData\\as_Gao\\as_rel_gao_20191203.txt'
    # as_gao_list = gain_as_rel_gao_v2(file_in_gao)
    # print(as_gao_list)
    as_vertex_compare(file_in_caida, file_in_gao)
    # save_path = '..\\000LocalData\\as_Gao\\as_rel_gao_20200221.txt'
    # write_to_csv(as_gao_list, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


"""
C:\Python37\python.exe D:/Code/Crawler4Caida/020MultiSourceCompare/as_compare_v2.py
Test Caida Source Data
Caida Source Active As: 67612
AS Up Stream Dict Length: 67530
AS Down Stream Dict Length: 13639
AS Stream Set Union Length: 67612
- - - - - - - - - - - - - - - - - - - -
Test Gao Source Data
Gao File All lines: 69695
AS Gao Stream Dict Up: 69695
AS Gao Stream Dict Down: 11803
AS Gao Set Union Length: 69695
- - - - - - - - - - - - - - - - - - - -
AS Intersection Length: 67398
AS Caida Difference Set Length: 214
AS Gao Difference Set Length: 2297

"""