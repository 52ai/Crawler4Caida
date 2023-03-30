# coding:utf-8
"""
create on Mar 30, 2023 By Wayne YU

Function:

按国家或区域提取该地区的TOP网络(按照IP地址量排名)，分析这些网络间的通路，测算比例

cn、belt_and_road、nato、us、bay、asean、af

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
    csv_file = open(des_path, 'w', newline='', encoding='utf-8')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country_caida():
    """
    根据Caida asn info获取as对应的国家信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_country = line[-1]
        as2country[as_number] = as_country
    return as2country


def gain_as2org_caida():
    """
    根据Caida asn info获取as对应的org信息
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info_from_caida.csv'
    as2org_dic = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        # print(line)
        as_number = line[0]
        as_org = line[2] + "," + line[1]
        as2org_dic[as_number] = as_org
    return as2org_dic


def gain_topn_as_list():
    """

    根据IPv4地址排名，获取各个Group的as_list
    cn、belt_and_road、nato、us、bay、asean、af
    :return global_as_ip_dict:
    :return group_country_dict:
    """
    global_as_ip_dict = {}
    with open("../000LocalData/ReCNNIC/global_as_ip_result.csv", "r", encoding="utf-8") as f:
        for item in f.readlines()[1:]:
            item = item.strip().split(",")
            global_as_ip_dict[item[0].strip("AS")] = int(item[-1])
    # print(global_as_ip_dict)
    """
    找出belt_and_road、asean、af中TOP 10的节点
    """

    group_country_dict = {"asean": [],
                          "bay": [],
                          "belt_and_road": [],
                          "nato": []}
    with open("../000LocalData/ReCNNIC/Country-Locations-Group - ReCNNIC.csv", "r", encoding="gbk") as f:
        for item in f.readlines()[1:]:
            item = item.strip().split(",")
            if item[7] == "1":
                group_country_dict["asean"].append(item[4])
            if item[8] == "1":
                group_country_dict["bay"].append(item[4])
            if item[9] == "1":
                group_country_dict["belt_and_road"].append(item[4])
            if item[10] == "1":
                group_country_dict["nato"].append(item[4])
    # print(group_country_dict)

    return global_as_ip_dict, group_country_dict


def rib_analysis(rib_file):
    """
    分析外连通路，途径国家情况
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    as2org_dic = gain_as2org_caida()
    global_as_ip_dict, group_country_dict = gain_topn_as_list()

    file_read = open(rib_file, 'r', encoding='utf-8')
    all_prefix_num = 0  # 统计国内节点，采集到的全部路由条目
    except_info_list = []  # 存储异常记录信息
    to_belt_and_road_path = []  # 存储所有去往b&r方向的路径
    to_belt_and_road_path_nato = []  # 存储所有去往b&r方向，经nato绕的节点
    to_belt_and_road_path_us = []  # 存储所有去往b&r方向，经us绕的节点
    for line in file_read.readlines():
        line = line.strip().split("|")
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            # 剔除全零路由
            continue
        all_prefix_num += 1
        # print(line)
        origin_country = "ZZ"

        try:
            origin_country = as2country_dic[str(as_path[-1])]
        except Exception as e:
            except_info_list.append(e)
        if origin_country in group_country_dict["belt_and_road"]:
            # print("origin:", origin_country)
            path_country = []
            for item_as in as_path:  # 遍历as path，获取途径国家
                item_country = "ZZ"
                try:
                    item_country = as2country_dic[str(item_as)]
                except Exception as e:
                    except_info_list.append(e)

                if item_country == "":
                    item_country = "ZZ"
                path_country.append(item_country)
            # print(path_country)
            # print(path_country[1:-1])
            if len(set(path_country[1:-1]).intersection(set(group_country_dict["nato"]))) != 0:
                to_belt_and_road_path_nato.append(path_country)
            if "US" in path_country[1:-1]:
                to_belt_and_road_path_us.append(path_country)
            to_belt_and_road_path.append(path_country)

    print("RIB All:", all_prefix_num)
    print("# to belt and road All:", len(to_belt_and_road_path))
    print("经NATO：", len(to_belt_and_road_path_nato), "占比:", len(to_belt_and_road_path_nato)/len(to_belt_and_road_path))
    print("经US：", len(to_belt_and_road_path_us), "占比:", len(to_belt_and_road_path_us)/len(to_belt_and_road_path))


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\BGPData\\rib_live\\rib_2023-01-13_181.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
