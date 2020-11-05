# coding: utf-8
"""
create on Nov 5, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据输入的上海、杭州ISP AS号码，统计与其相连的自治域网络号码及其所属企业名称
"""
import csv
import time


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


def analysis(as_list):
    """
    根据输入的as list,统计与其相连的AS网络（CN）
    :param as_list:
    :return rel_as_list:
    """
    rel_as_list = []
    as_rel_file = "../000LocalData/as_relationships/serial-1/20200701.as-rel.txt"
    file_read = open(as_rel_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        if line.strip().find("#") == 0:
            continue
        line = line.strip().split('|')
        print(line)
        if line[0] in as_list and line[1] not in as_list:
            rel_as_list.append(line[1])
        elif line[1] in as_list and line[0] not in as_list:
            rel_as_list.append(line[0])

    return rel_as_list


if __name__ == "__main__":
    time_start = time.time()
    as_group = ["4134"]
    potential_as = analysis(as_group)
    print(potential_as)
    print("LEN OF POTENTIAL AS:", len(potential_as))
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")