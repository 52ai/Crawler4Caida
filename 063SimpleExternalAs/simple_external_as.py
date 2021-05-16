# coding:utf-8
"""
create on May 16, 2021 By Wenyan Yu
Email: ieeflsyu@outlook.com

Function:

统计当前国际TOP10网络和国内TOP10网络对外互联网络数量和国家数量
为了简化只需要统计每个AS的AS Name，all_relationships, external_relationships, external_country, country

"""
import os
import time
import csv

file_path = "../000LocalData/as_relationships/serial-1/20210501.as-rel.txt"
as_info_file = '../000LocalData/as_Gao/asn_info.txt'


def write_to_csv(res_list, des_path, title_line):
    """
    把给定的List，写到指定路径的文件中
    :param res_list:
    :param des_path:
    :param title_line:
    :return: None
    """
    print("write file <%s> ..." % des_path)
    csv_file = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(title_line)
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()
    print("write finish!")


def gain_as2country():
    """
    根据as info file信息获取AS与国家的对应字典
    :return as2country:
    :return as2info:
    """
    as2country = {}  # 存储as号到country的映射关系
    as2info = {}  # 存储as号到info的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        as_number = line[0]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = as_country
        as2info[as_number] = line[1]
    return as2country, as2info


def gain_active_as(open_file):
    """
    根据输入的AS互联关系数据，获取当前时间活跃的AS列表
    :param open_file:
    :return date_str:
    :return as_list:
    """
    print(open_file)
    # 处理文件名，提取日期信息
    temp_str = open_file.split('/')[-1]
    date_str = temp_str.split(".")[0]
    file_read = open(open_file, 'r', encoding='utf-8')
    as_list = []  # 存储当前时间，全部有连接关系的AS
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        as_list.append(line.strip().split('|')[0])
        as_list.append(line.strip().split('|')[1])
    as_list = list(set(as_list))  # 先转换为字典，再转化为列表，速度还可以
    as_list.sort(key=lambda i: int(i))
    return date_str, as_list


def gain_simple_external_as(asn_list, open_file):
    """
    根据传入的asn_list，统计其simple external as
    AS Name，all_relationships, external_relationships, external_country, country, as_info
    :param asn_list:
    :param open_file:
    :return rel:
    """
    as2country, as2info = gain_as2country()  # 获取as到国家的字典
    as_rel_dict = {}  # 存储as互联关系及国别
    except_item = []  # 存储异常的项目
    for asn_item in asn_list:
        as_rel_dict.setdefault(asn_item, []).append(0)  # 存储总的互联关系数量
        as_rel_dict.setdefault(asn_item, []).append(0)  # 存储外部互联关系数量
        as_rel_dict.setdefault(asn_item, []).append([])  # 存储外部互联国家列表
        as_rel_dict.setdefault(asn_item, []).append("")  # 存储国别信息
        as_rel_dict.setdefault(asn_item, []).append("")  # 存储info

    # 遍历bgp互联关系列表，统计as互联关系
    file_read = open(open_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        as_rel_dict[line[0]][0] += 1
        as_rel_dict[line[1]][0] += 1

        as0_country = "other"
        as1_country = "other"

        as0_info = "None"
        as1_info = "None"

        try:
            as0_country = as2country[line[0]]
            as0_info = as2info[line[0]]
        except Exception as e:
            except_item.append(e)

        try:
            as1_country = as2country[line[1]]
            as1_info = as2info[line[1]]
        except Exception as e:
            except_item.append(e)

        # 如果as0和as1不属于同一个国家，则为外部链接，二者external_relationships均需加1
        # 同把国家加到对方的国家列表中
        if as0_country != as1_country:
            """
            外部互联
            """
            as_rel_dict[line[0]][1] += 1
            as_rel_dict[line[1]][1] += 1

            as_rel_dict[line[0]][2].append(as1_country)
            as_rel_dict[line[1]][2].append(as0_country)

        # 所有情况均需更新country和info
        as_rel_dict[line[0]][3] = as0_country
        as_rel_dict[line[1]][3] = as1_country

        as_rel_dict[line[0]][4] = as0_info
        as_rel_dict[line[1]][4] = as1_info

    print("异常数量:", len(except_item))

    result_list = []  # 存储全球结果列表
    result_list_cn = []  # 存储中国结果列表
    for key in as_rel_dict.keys():
        # print(as_rel_dict[key])
        asn = key
        all_rel = as_rel_dict[key][0]
        external_rel = as_rel_dict[key][1]
        external_country = len(list(set(as_rel_dict[key][2])))
        as_country = as_rel_dict[key][3]
        as_info = as_rel_dict[key][4]

        result_list.append([asn, all_rel, external_rel, external_country, as_country, as_info])

        if as_country == "CN":
            result_list_cn.append([asn, all_rel, external_rel, external_country, as_country, as_info])

    print("全球Simple External AS记录：", len(result_list))
    print("中国Simple External AS记录：", len(result_list_cn))

    # 对记录进行排序
    result_list.sort(reverse=True, key=lambda elem: int(elem[1]))
    result_list_cn.sort(reverse=True, key=lambda elem: int(elem[1]))
    print("国际TOP AS对外互联网络数量及国家数量：")
    for item in result_list[0:10]:
        print(item)
    print("国内TOP AS对外互联网络数量及国家数量：")
    for item in result_list_cn[0:10]:
        print(item)

    save_path = "../000LocalData/as_map_simple/global_top10.csv"
    write_to_csv(result_list[0:10],
                 save_path,
                 ["asn", "all_rel", "external_rel", "external_country", "as_country", "as_info"])
    save_path = "../000LocalData/as_map_simple/china_top10.csv"
    write_to_csv(result_list_cn[0:10],
                 save_path,
                 ["asn", "all_rel", "external_rel", "external_country", "as_country", "as_info"])


if __name__ == "__main__":
    time_start = time.time()  # 记录启动的时间
    date_string, as_active_list = gain_active_as(file_path)
    print("时间：", date_string)
    print("活跃AS网络:", len(as_active_list))
    gain_simple_external_as(as_active_list, file_path)
    print("=>Scripts Finish, Time Consuming:", (time.time() - time_start), "S")
