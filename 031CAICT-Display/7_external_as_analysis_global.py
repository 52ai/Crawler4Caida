# coding:utf-8
"""
create on June 17, 2020 By Wayne YU

Function:

参考我国出口AS互联关系统计（互联国家+互联关系总数）（直接绘制1998-2019）程序
新增全球其他国家出口AS互联关系统计程序

主要关注
美国（US），俄罗斯（RU），德国（DE），法国（FR），日本（JP）
巴西（BR），印度（IN），越南（VN），印尼（ID），泰国（TH）

"""

import time
import csv
import os


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
        writer = csv.writer(csv_file, delimiter="|")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_country_info():
    """
    根据国家的缩写，翻译为中文
    :return country_info_dict:
    """
    geo_file = '../000LocalData/as_geo/GeoLite2-Country-Locations-zh-CN.csv'
    country_info_dict = {}
    file_read = open(geo_file, 'r', encoding='gbk')
    for line in file_read.readlines():
        line = line.strip().split(',')
        # print(line)
        country_info_dict[line[4]] = line[5]
    return country_info_dict


def gain_as2country(as_info_file, target_country):
    """
    根据传入的as info file信息获取AS与国家的对应字典及该国家的所有的AS Info
    :param as_info_file:
    :param target_country:
    :return as2country:
    """
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
    return as2country


def external_as_analysis(target_country, as2country):
    """
    根据输入的国家，统计该国家的出口AS数量及其互联方向的统计分析
    :param target_country:
    :param as2country:
    :return:
    """
    as2country_cn = gain_country_info()
    print(as2country_cn[target_country])
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
        country_as_list = []  # 存储该国的活跃AS号
        external_country_list = []  # 存储该国出口方向的国家
        for line in file_read.readlines():
            if line.strip().find("#") == 0:
                continue
            try:
                if as2country[str(line.strip().split('|')[0])] == target_country:
                    country_as_list.append(str(line.strip().split('|')[0]))  # 统计该国活跃as网络数量
                if as2country[str(line.strip().split('|')[1])] == target_country:
                    country_as_list.append(str(line.strip().split('|')[1]))  # 统计该国活跃as网络数量

                if as2country[str(line.strip().split('|')[0])] == target_country:
                    if as2country[str(line.strip().split('|')[1])] != target_country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[0]))
                        external_country_list.append(as2country[str(line.strip().split('|')[1])])
                else:
                    if as2country[str(line.strip().split('|')[1])] == target_country:
                        external_cnt += 1
                        external_as_list.append(str(line.strip().split('|')[1]))
                        external_country_list.append(as2country[str(line.strip().split('|')[0])])
            except Exception as e:
                # print(e)
                pass
        external_as_list = list(set(external_as_list))
        print("Country Active AS Count:", len(list(set(country_as_list))))
        print("External Edges Count:", external_cnt)
        print("External AS Count:", len(external_as_list))
        print("External Country Count:", len(list(set(external_country_list))))
        # print(list(set(external_country_list)))

        # 统计互联国家方向的排名
        external_country_rank = {}
        for item in list(set(external_country_list)):
            external_country_rank[item] = 0
        for item in external_country_list:
            external_country_rank[item] += 1
        # print(len(external_country_rank))
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
        temp_str = path_item.split('\\')[-1]
        date_str = str(temp_str).split('.')[0]
        save_path = "../000LocalData/caict_display/External/" + target_country + "_external" + str(date_str) + ".csv"
        write_to_csv(external_country_rank_list, save_path)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动时间
    # country_list = ["CN", "US", "DE", "JP", "KR",
    #                 "BR", "IN", "RU", "ZA", "SG",
    #                 "MY", "ID", "VN", "FR", "TH"]
    country_list = ["CA"]
    as_info_file_in = '..\\000LocalData\\as_Gao\\asn_info.txt'
    for country in country_list:
        as2country_dict = gain_as2country(as_info_file_in, country)
        external_as_analysis(country, as2country_dict)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")
