# coding: utf-8
"""
create on Nov 5, 2020 By Wenyan YU
Email: ieeflsyu@outlook.com

Function:

根据输入的上海、杭州ISP AS号码，统计与其相连的自治域网络号码及其所属企业名称

AS56041 浙江移动
AS58461 杭州电信IDC

AS17621 上海联通
AS24400 上海移动
AS4811 上海电信
AS4812 上海电信
AS24400 东方有线

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
    csvFile = open(des_path, 'w', newline='', encoding='gbk')
    try:
        writer = csv.writer(csvFile, delimiter=",")
        for i in res_list:
            writer.writerow(i)
    except Exception as e:
        print(e)
    finally:
        csvFile.close()
    print("write finish!")


def gain_as2country():
    """
    根据as info file信息获取AS与国家的对应字典
    :return as2country:
    """
    as_info_file = '..\\000LocalData\\as_Gao\\asn_info.txt'
    as2country = {}  # 存储as号到country的映射关系
    file_read = open(as_info_file, 'r', encoding='utf-8')
    for line in file_read.readlines():
        line = line.strip().split("\t")
        # print(line)
        as_number = line[0]
        as_info = line[1]
        as_country = line[1].strip().split(",")[-1].strip()
        as2country[as_number] = [as_info, as_country]
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
        # print(line)
        if line[0] in as_list and line[1] not in as_list:
            rel_as_list.append([line[1], line[0]])
        elif line[1] in as_list and line[0] not in as_list:
            rel_as_list.append([line[0], line[1]])

    return rel_as_list


if __name__ == "__main__":
    time_start = time.time()
    as_group = ["56041", "58461", "17621", "24400", "4811", "4812", "24400"]
    potential_as = analysis(as_group)
    print("LEN OF POTENTIAL AS:", len(potential_as))
    as2info = gain_as2country()
    potential_as_list_info = []  # 存储潜在的AS信息
    save_file_path = "./potential_as.csv"
    for item in potential_as:
        try:
            if as2info[item[0]][1] == "CN":
                # print(item[0], as2info[item[0]][0], item[1], as2info[item[1]][0])
                potential_as_list_info.append([item[0], as2info[item[0]][0], item[1], as2info[item[1]][0]])
        except Exception as e:
            print(e)
    write_to_csv(potential_as_list_info, save_file_path)
    time_end = time.time()
    print("=>Scripts Finish, Time Consuming:", (time_end - time_start), "S")