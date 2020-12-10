# coding:utf-8
"""
create on Dec 10, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

新的展示界面，需要统计新的数据
该程序用于统计全国及全球TOP自治域网络互联地图，选中某个节点，可向下钻取获取该网络的互联关系。

处理思路
1）使用最新的as_relationships获取as网络的排名
2）使用asn_info获取as的具体信息
3）输出TOP AS之间的互联关系，及其向下钻取的网络互联关系
"""

import time
import csv


def write_to_csv(res_list, des_path):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :return None:
    """
    print("write file <%s>..." % des_path)
    csv_file = open(des_path, "w", newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_active_as(open_file):
    """
    根据输入的as互联关系数据，获取当前时间活跃的AS列表
    :param open_file:
    :return:
    """
    print(open_file)
    as_list = []  # 存储当前时间，全部有连接关系的AS
    file_read = open(open_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find('#') == 0:
            continue
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转换为列表
    as_list.sort(key=lambda i: int(i))
    return as_list


def gain_as_relationships_dict(asn_list, open_file):
    """
    根据传入的asn_list，统计其bgp互联关系（All, Peer, Transit）
    :param asn_list:
    :param open_file:
    :return rel:
    """
    as_rel_dict = {}  # 存储as互联关系统计结果
    # 根据asn_list生成原始字典
    # 构造原始字典中的list时，有一定的讲究，否则就是个坑
    # dict_value = [0, 0, 0, 0] # edge_cnt、peer_cnt、transit_provider_cnt、transit_customer_cnt
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
        if line[2] == '0':  # 如果该条关系为peer的关系
            # 总连接数自增1
            as_rel_dict[line[0]][0] += 1
            as_rel_dict[line[1]][0] += 1
            # Peer连接数自增1
            as_rel_dict[line[0]][1] += 1
            as_rel_dict[line[1]][1] += 1
        elif line[2] == '-1':  # 否则该条关系为transit关系
            # 总连接数自增1
            as_rel_dict[line[0]][0] += 1
            as_rel_dict[line[1]][0] += 1
            # provider-customer, transit关系分别自增1
            as_rel_dict[line[0]][2] += 1
            as_rel_dict[line[1]][3] += 1
    return as_rel_dict


def gain_as_info(asn_core_map_list):
    """
    根据asn info文件，去获取as的详细信息

    :param asn_core_map_list:
    :return asn_core_map_list:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info.txt'
    as2info = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_info = line[1]
        as_country = line[1].strip().split(",")[-1].strip()
        as2info[as_number] = [as_info, as_country]
    # 根据as2info哈希表，生成as_core_map_list
    except_asn = []  # 存储没有信息的asn
    asn_core_map_list_copy = []
    for item in asn_core_map_list:
        try:
            item.extend(as2info[item[0]])
            asn_core_map_list_copy.append(item)
        except Exception as e:
            # print(e, item[0])
            temp_info = ["/", "/"]
            item.extend(temp_info)
            asn_core_map_list_copy.append(item)
            except_asn.append(item[0])
    # 输出没有信息的asn号
    print("没有信息的asn号个数:", len(set(except_asn)))
    asn_core_map_list = asn_core_map_list_copy
    return asn_core_map_list


if __name__ == "__main__":
    time_start = time.time()
    as_rel_file = "../000LocalData/as_relationships/serial-1/20201101.as-rel.txt"
    as_active_list = gain_active_as(as_rel_file)
    print("活跃的AS网络数量：", len(as_active_list))
    # 直接遍历一次，获取全部的互联信息
    active_as_rel_dict = gain_as_relationships_dict(as_active_list, as_rel_file)
    # print(active_as_rel_dict)
    # 遍历active_as_rel_dict 生成as_core_map_data
    list_temp = []
    as_core_map_data = []
    for key in active_as_rel_dict:
        list_temp.append(key)
        list_temp.extend(active_as_rel_dict[key])
        as_core_map_data.append(list_temp)
        list_temp = []
    as_core_map_data = gain_as_info(as_core_map_data)
    as_core_map_data.sort(reverse=True, key=lambda elem: int(elem[1]))  # 以全部互联关系进行排序
    # print(as_core_map_data[0:1000])
    save_path = '..\\000LocalData\\BGPMonitor\\as_core_map_data.csv'
    write_to_csv(as_core_map_data, save_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
