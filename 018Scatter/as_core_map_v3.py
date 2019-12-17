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


def gain_as_info(asn_core_map_list):
    """
    根据as_org_info文件，去获取as的详细信息
    包括AS_Name、Org_Name、Source、Country、Latitude、Longitude
    :param asn_core_map_list:
    :return as_core_map_list:
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
    # print(as_org_info_dict)
    # 根据as org info哈希表，生成asn_core_map_list信息
    except_asn = []  # 存储没有信息的asn
    asn_core_map_list_copy = []
    for item in asn_core_map_list:
        try:
            item.extend(as_org_info_dict[item[0]])
            asn_core_map_list_copy.append(item)
        except Exception as e:
            # print(e, item[0])
            except_asn.append(item[0])
    # 输出没有信息的asn号
    print("没有信息的asn号个数:", len(set(except_asn)))
    print(set(except_asn))
    asn_core_map_list = asn_core_map_list_copy
    return asn_core_map_list


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    active_as = []  # 记录活跃的as号
    file_path = []
    for root, dirs, files in os.walk("..\\000LocalData\\as_relationships\\serial-1"):
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
            # print(list_temp)
            as_core_map_data.append(list_temp)
            list_temp = []
        # print(as_core_map_data)
        as_core_map_data = gain_as_info(as_core_map_data)
        # print(as_core_map_data)
        # 存储as_core_map_data文件
        save_path = '..\\000LocalData\\as_map\\as_core_map_data_new' + date_string + '.csv'
        write_to_csv(as_core_map_data, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")


"""
1998年全球BGP互联数据中，无法获取信息的asn号个数: 161
{'6676', '8573', '7040', '2135', '8277', '5393', '5465', '3605', '7910', '8198', '5559', '5506', '8355', '3586', '6840', '8417', '4039', '5471', '5561', '6746', '6758', '5509', '8421', '5412', '7414', '6683', '5510', '6680', '5490', '6865', '6722', '8212', '6897', '8370', '6795', '8306', '6875', '7124', '8252', '834', '6678', '8413', '6517', '6705', '6809', '6743', '7346', '8498', '8533', '1899', '2853', '3248', '6765', '6741', '6806', '5590', '6770', '8465', '7642', '3353', '6901', '5569', '3350', '6515', '5556', '2120', '5597', '8514', '10278', '5395', '6864', '5611', '8205', '5492', '6589', '8349', '6668', '6708', '6684', '8511', '5639', '8366', '2820', '3346', '8392', '8407', '3228', '5481', '6888', '8383', '5558', '3208', '8199', '5499', '6771', '8293', '8509', '8504', '5595', '7837', '6889', '8335', '6690', '8215', '7864', '6804', '6902', '8320', '5625', '6752', '5557', '8313', '10292', '8583', '8225', '7984', '8497', '2380', '6715', '8425', '5536', '8259', '8321', '8332', '8250', '6884', '6792', '6896', '5494', '7420', '6543', '8424', '8397', '6845', '6835', '8316', '3251', '6754', '5402', '6568', '6841', '8406', '10269', '6669', '6827', '8209', '5592', '6721', '3328', '8340', '5596', '6800', '8525', '5512', '6064', '8284', '8327', '6756', '6760', '5389', '6783'}


"""