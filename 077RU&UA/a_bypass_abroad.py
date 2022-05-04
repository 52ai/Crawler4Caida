# coding:utf-8
"""
create on May 4, 2022 By Wayne YU

Function:

从国际IP Prefix角度，统计三家企业上游网络的重合度，结果为3（完全不重合）、2（任意两个重合）、1（完全重合）

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


def rib_analysis(rib_file):
    """
    分析RIB数据，统计4134、4837以及9808，出国第一跳的重合度
    :param rib_file:
    :return:
    """
    as2country_dic = gain_as2country_caida()
    print("AS4134's Country:", as2country_dic['4134'])
    file_read = open(rib_file, 'r', encoding='utf-8')
    aim_as_list = ["4134", "4837", "9808"]
    abroad_v4_prefix = {}  # 统计每个国际路由中三家的as_path
    except_info_list = []  # 存储异常记录
    for line in file_read.readlines():
        line = line.strip().split("|")
        aim_as = line[4]
        v4_prefix = line[5]
        as_path = line[-2].split(" ")
        if str(v4_prefix).find("0.0.0.0/0") != -1:
            print(v4_prefix)
            continue
        origin_country = "ZZ"
        try:
            origin_country = as2country_dic[str(as_path[-1])]
        except Exception as e:
            except_info_list.append(e)

        if aim_as in aim_as_list and origin_country != "CN":
            # print(aim_as, v4_prefix, origin_country, as_path)
            if v4_prefix not in abroad_v4_prefix.keys():
                abroad_v4_prefix[v4_prefix] = [as_path]
            else:
                abroad_v4_prefix[v4_prefix].append(as_path)

    print("国际v4路由条目数：", len(abroad_v4_prefix.keys()))

    result_list = []  # 存储结果数据[国际路由，三家上游AS重合度分析结果]
    """
    3:代表完全不重合，221073
    2:代表有两家存在重合，454812
    1:代表三家完全重合，193165
    
    共计809650
    """
    for key in abroad_v4_prefix.keys():
        temp_list = []  # 用于存储出国第一跳的AS
        for path_item in abroad_v4_prefix[key]:
            print(path_item)
            if "58453" in path_item:
                temp_list.append(path_item[2])
            else:
                temp_list.append(path_item[1])
        print(key, temp_list, len(set(temp_list)))
        result_list.append([key, len(set(temp_list))])

    save_file = "..\\000LocalData\\RU&UA\\a_bypass_abroad.csv"
    write_to_csv(result_list, save_file)


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    rib_analysis("..\\000LocalData\\RU&UA\\rib\\z20220320.txt")
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")