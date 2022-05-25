# coding:utf-8
"""
create on May 25, 2022 By Wayne YU
Email: ieeflsyu@outlook.com

Function:

统计CN国际路由依赖情况，明确为出国第一跳的国家

"""
import time
import csv
from IPy import IP


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


def gain_country2group():
    """
    根据geo信息，输出每个国家对应的Group信息，如欧洲、亚太、一带一路等
    :return country2group:
    """
    country_2_group_file = '..\\000LocalData\\as_geo\\Country-Locations-Group-4wx.csv'
    country2group_dict = {}  # 存储国家到Group的映射关系
    file_read = open(country_2_group_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split(",")
        if line[0] == "ID":
            # print(line)
            continue
        if line[4] not in country2group_dict.keys():
            country2group_dict[line[4]] = line
    return country2group_dict


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


def rib_analysis(rib_file):
    """
    分析RIB数据，统计我国际路由获取情况，输出Excel中间值，规范化处理
    :return:
    """
    print(rib_file)

    as2country = gain_as2country_caida()
    as2org = gain_as2org_caida()
    country2group = gain_country2group()

    file_read = open(rib_file, 'r', encoding='utf-8')
    all_v4_prefix = []  # 存储国内节点采集到的全部路由条目
    all_v4_num = 0  # 存储全部的v4量
    except_info_list = []  # 存储异常记录信息
    direct_route_country_dict = {}  # 按国家维度存储直联路由依赖情况
    for line in file_read.readlines():
        line = line.strip().split("|")
        # if line[4] != "4134":
        #     continue
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue
        country_path = []  # 将as_path转换成国家path
        for as_item in as_path:
            if as_item.find("{") != -1:
                as_item = as_item.strip("{").strip("}").split(",")[0]
            country_str = "ZZ"
            try:
                country_str = as2country[str(as_item)]
            except Exception as e:
                except_info_list.append(e)
                # print(e)
            country_path.append(country_str)

        all_v4_prefix.append(v4_prefix)
        all_v4_num += len(IP(v4_prefix))
        # print(v4_prefix, as_path, country_path)
        """
        按国家维度，构建我国际路由获取依赖情况
        """
        direct_route_country = "ZZ"
        for country_item in country_path:
            if country_item != "CN":
                direct_route_country = country_item
                break
        if direct_route_country not in direct_route_country_dict.keys():
            direct_route_country_dict[direct_route_country] = len(IP(v4_prefix))
        else:
            direct_route_country_dict[direct_route_country] += len(IP(v4_prefix))

    print("国内节点采集路由条目总数：", len(all_v4_prefix))
    print("国内节点采集路由条目总数(去重后)：", len(set(all_v4_prefix)))
    print("国内各骨干节点采集v4地址总量：", all_v4_num)
    print("ASN字典异常记录：", len(set(except_info_list)))
    direct_route_country_list = []  # 将国家维度的路由依赖转换为列表
    for item in direct_route_country_dict.keys():
        direct_route_country_list.append([item,
                                          direct_route_country_dict[item]])
    print("国家或地区数量:", len(direct_route_country_list))
    direct_route_country_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    direct_route_country_result = []  # 存储结果
    for item in direct_route_country_list:
        continent = country2group[str(item[0])][3]
        country_name = country2group[str(item[0])][5]
        is_belt_and_road = country2group[str(item[0])][7]
        is_asia_pacific = country2group[str(item[0])][8]
        belt_and_road_str = "其他"
        asia_pacific_str = "其他"

        if is_belt_and_road == "1":
            belt_and_road_str = "一带一路"
        if is_asia_pacific == "1":
            asia_pacific_str = "亚太"

        temp_line = [item[0], country_name, continent, belt_and_road_str, asia_pacific_str, item[1], round(item[1]/all_v4_num, 4)]
        direct_route_country_result.append(temp_line)
        print(temp_line)
    save_file = "direct_route_country_result.csv"
    write_to_csv(direct_route_country_result, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录程序启动时间
    rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220320.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start))





