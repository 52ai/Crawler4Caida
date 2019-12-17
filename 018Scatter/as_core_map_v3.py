# coding:utf-8
"""
create on Dec 11, 2019 By Wayne Yu

Version:3.0
Description：优化了算法，大大缩短了遍历图计算关键参数的时间
哈希表(Python下就是字典了)的时间复杂度简直不要太好了，能有字典解决的，就不要无脑循环了
明明可以遍历一遍表即可获取到全部信息的，之前非得循环套循环，哎……

"""
import os
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
    return as_rel_dict


def gain_as_info(asn):
    """
    根据as-org2info文件，去获取as的详细信息
    :param asn:
    :return as_info_list:
    """
    as_info_list = []
    as_org2info_file = "..\\000LocalData\\as_geo\\20190701.as-org2info.txt"
    as_org2info_asn_file = "..\\000LocalData\\as_geo\\20190701.as-org2info-asn.txt"
    as_org2info_read = open(as_org2info_file, 'r', encoding='utf-8')
    as_org2info_asn_read = open(as_org2info_asn_file, 'r', encoding='utf-8')
    org_id = ""
    for line in as_org2info_asn_read.readlines():
        if line.strip().split("|")[0] == asn:
            org_id = line.strip().split("|")[3]
            as_info_list.append( line.strip().split("|")[2])  # as name
            break
    for line in as_org2info_read.readlines():
        if line.strip().split("|")[0] == org_id:
            as_info_list.append(line.strip().split("|")[2])  # org name
            as_info_list.append(line.strip().split("|")[4])  # source
            as_info_list.append(line.strip().split("|")[3])  # country
            break
    return as_info_list


def gain_as_geo(asn_country):
    """
    根据传入的as国家（地区信息）获取其经纬度
    :param asn_country:
    :return geo_list:
    """
    geo_file = "..\\000LocalData\\as_geo\\201603.locations.txt"
    geo_list = []
    file_read = open(geo_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as_country = line.strip().split("|")[2]
        if as_country == asn_country:
            geo_list.append(line.strip().split("|")[5])  # 获取维度
            geo_list.append(line.strip().split("|")[6])  # 获取经度
            return geo_list  # 找到后直接结束函数，并返回
    # 没有找到则设置一个默认值
    print(asn_country, "is not found in geo file!")
    geo_list.append("0.0")
    geo_list.append("0.0")
    return geo_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    active_as = []  # 记录活跃的as号
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-3"):
        for file_item in files:
            file_path.append(os.path.join(root, file_item))
    # print(file_path)
    as_core_map_data = []
    for path_item in file_path:
        date_string, as_active_list = gain_active_as(path_item)
        print("活跃的AS号数量：", len(as_active_list))
        # print(as_active_list)
        as_core_map_data = []
        # 直接遍历一次图，获取全部的互联信息
        active_as_rel_dict = gain_as_relationships_dict(as_active_list, path_item)
        # print(active_as_rel_dict)
        # 遍历active_as_rel_dict 生成as_core_map_data
        list_temp = []
        for key in active_as_rel_dict:
            list_temp.append(key)
            list_temp.extend(active_as_rel_dict[key])
            # as_info = gain_as_info(key)  # 获取as info
            # list_temp.extend(as_info)
            # as_geo = gain_as_geo(as_info[-1])
            # list_temp.extend(as_geo)
            print(list_temp)
            as_core_map_data.append(list_temp)
            list_temp = []
        # 存储as_core_map_data文件
        save_path = '..\\000LocalData\\as_map\\as_core_map_data_new' + date_string + '.csv'
        write_to_csv(as_core_map_data, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
